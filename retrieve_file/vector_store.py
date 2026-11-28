import sqlite3
import numpy as np
import faiss            # vector similarity search linrary-> stores vectors in a searchable index n find similar vectors

from .config import DB_PATH, INDEX_PATH, IDS_PATH
from .embeddings import generate_embedding
from .chunker import chunk_text

def build_index():
    with sqlite3.connect(DB_PATH) as conn:
        files = conn.execute("""
            SELECT id, name, content
            FROM files
            WHERE content IS NOT NULL
              AND content != ''
        """).fetchall()

    if not files:
        raise ValueError(
            "No searchable files found. Add supported text files before indexing."
        )

    embeddings = []
    file_ids = []

    for file_id, name, content in files:

        # Split file content into chunks
        chunks = chunk_text(content)

        for chunk in chunks:

            # Generate one embedding per chunk
            vector = generate_embedding(chunk)

            embeddings.append(vector)

            # Multiple chunks can belong to the same file
            file_ids.append(file_id)

        print(f"Embedded: {name} ({len(chunks)} chunks)")

    vectors = np.array(embeddings, dtype="float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(vectors)

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    # Save FAISS index and chunk-to-file mapping
    faiss.write_index(index, str(INDEX_PATH))
    np.save(IDS_PATH, np.array(file_ids, dtype=np.int64))

    print(
        f"Indexed {len(files)} files "
        f"into {index.ntotal} chunks."
    )


if __name__ == "__main__":
    build_index()