import sqlite3
import numpy as np
import faiss            # vector similarity search linrary-> stores vectors in a searchable index n find similar vectors

from database import DB_PATH
from embeddings import generate_embedding

def build_index():
    with sqlite3.connect(DB_PATH) as conn:
        files = conn.execute("""
            SELECT id, name, content
            FROM files
            WHERE content IS NOT NULL
                AND content != ''
        """).fetchall()

    if not files:
        print("No files available for indexing.")
        return

    embeddings = []
    file_ids = []

    for file_id, name, content in files:
        vector = generate_embedding(content)

        embeddings.append(vector)
        file_ids.append(file_id)

        print(f"Embedded: {name}")

    vectors = np.array(embeddings, dtype="float32")

    faiss.normalize_L2(vectors)

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, "data/files.index")
    np.save("data/file_ids.npy", np.array(file_ids))

    print(f"Indexed {index.ntotal} files.")

if __name__ == "__main__":
    build_index()