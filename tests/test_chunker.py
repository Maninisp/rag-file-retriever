from retrieve_file.chunker import chunk_text
from retrieve_file.embeddings import get_model

text = (
    "Python is used for backend development. "
    "FastAPI supports REST APIs. "
    "JWT handles authentication. "
    "PostgreSQL stores application data. "
) * 30

chunks = chunk_text(
    text,
    chunk_size=200,
    overlap_percent=0.20
)

tokenizer = get_model().tokenizer

for i, chunk in enumerate(chunks, start=1):
    token_count = len(
        tokenizer.encode(chunk, add_special_tokens=False)
    )

    print(f"Chunk {i}: {token_count} tokens")