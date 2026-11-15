import sqlite3
import numpy as np
import faiss
from rich.console import Console
from rich.table import Table

from database import DB_PATH
from embeddings import generate_embedding

def semantic_search(query, top_k=3):
    # Load saved index and file ID mapping
    index = faiss.read_index("data/files.index")
    file_ids = np.load("data/file_ids.npy")

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


# if __name__ == "__main__":
#     query = "Find my animal healthcare application"

#     for result in semantic_search(query):
#         print(result)

if __name__ == "__main__":
    console = Console()

    query = input("Enter your search query: ")
    results = semantic_search(query)

    table = Table(title="AI File Retrieval Results")

    table.add_column("Rank", style="cyan")
    table.add_column("Filename", style="green")
    table.add_column("Location")
    table.add_column("Similarity", style="yellow")

    for rank, result in enumerate(results, start=1):
        table.add_row(
            str(rank),
            result["name"],
            result["path"],
            f'{result["score"]:.2%}'
        )

    console.print()
    console.print(f"[bold]Search:[/bold] {query}")
    console.print(table)