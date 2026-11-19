import sqlite3
from pathlib import Path

import numpy as np
import faiss

from .database import DB_PATH, BASE_DIR
from .embeddings import generate_embedding

def semantic_search(query, top_k=3):
    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
        raise ValueError("top_k must be a positive integer.")
    
    index_path = BASE_DIR/"data"/"files.index"
    ids_path = BASE_DIR/"data"/"file_ids.npy"

    if not index_path.is_file() or not ids_path.is_file():
        raise FileNotFoundError(
            "No search index found. Please index a folder first."
        )

    # Load saved index and file ID mapping
    index = faiss.read_index(str(index_path))
    file_ids = np.load(ids_path)

    if index.ntotal != len(file_ids):
        raise ValueError(
            "Search index is inconsistent. Please rebuild the index."
        )

    # Convert user query into an embedding
    query_vector = np.array(
        [generate_embedding(query)], dtype="float32"
    )   

    # Normalize query vector
    faiss.normalize_L2(query_vector)

    # Find top matching vectors
    scores, positions = index.search(query_vector, top_k)

    results = []

    with sqlite3.connect(DB_PATH) as conn:
        for score, position in zip(scores[0], positions[0]):
            if position == -1:
                continue

            file_id = int(file_ids[position])

            file = conn.execute("""
                SELECT name, path
                FROM files
                WHERE id = ?
            """, (file_id,)).fetchone()

            if file:
                results.append({
                    "name": file[0],
                    "path": file[1],
                    "score": float(score)
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
