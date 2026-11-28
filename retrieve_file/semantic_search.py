import sqlite3
from pathlib import Path

import numpy as np
import faiss

from .config import DB_PATH, INDEX_PATH, IDS_PATH
from .embeddings import generate_embedding

def semantic_search(query, top_k=3, threshold=0.20):
    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
        raise ValueError("top_k must be a positive integer.")

    if not isinstance(threshold, (int, float)) or isinstance(threshold, bool):
        raise ValueError("threshold must be a number.")

    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1.")

    if not INDEX_PATH.is_file() or not IDS_PATH.is_file():
        raise FileNotFoundError(
            "No search index found. Please index a folder first."
        )

    index = faiss.read_index(str(INDEX_PATH))
    file_ids = np.load(IDS_PATH)

    if index.ntotal != len(file_ids):
        raise ValueError(
            "Search index is inconsistent. Please rebuild the index."
        )

    query_vector = np.array(
        [generate_embedding(query)], dtype="float32"
    )

    faiss.normalize_L2(query_vector)

    # Search all chunks to guarantee top_k distinct files.
    scores, positions = index.search(query_vector, index.ntotal)

    # Store the highest score for each file ID.
    best_scores = {}

    for score, position in zip(scores[0], positions[0]):
        if position == -1:
            continue

        if score < threshold:
            continue

        file_id = int(file_ids[position])

        if file_id not in best_scores:
            best_scores[file_id] = float(score)
        else:
            best_scores[file_id] = max(
                best_scores[file_id],
                float(score)
            )

    # Sort files by their highest matching chunk score.
    ranked_files = sorted(
        best_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )[:top_k]

    results = []

    with sqlite3.connect(DB_PATH) as conn:
        for file_id, score in ranked_files:
            file = conn.execute("""
                SELECT name, path
                FROM files
                WHERE id = ?
            """, (file_id,)).fetchone()

            if file:
                results.append({
                    "name": file[0],
                    "path": file[1],
                    "score": score
                })

    return results

def group_by_project(results):
    projects = {}

    for result in results:
        file_path = Path(result["path"])

        project_name = file_path.parent.name
        project_path = str(file_path.parent)

        if project_path not in projects:
            projects[project_path] = {
                "project_name": project_name,
                "project_path": project_path,
                "files": [],
                "score": 0
            }

        projects[project_path]["files"].append({
            "name": result["name"],
            "path": result["path"],
            "score": result["score"]
        })
        
        projects[project_path]["score"] = max(
            projects[project_path]["score"],
            result["score"]
        )

    return sorted(
        projects.values(),
        key=lambda project: project["score"],
        reverse=True
    )
