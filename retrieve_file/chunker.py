from .embeddings import get_model


def chunk_text(text, chunk_size=200, overlap_percent=0.20):
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    if not 0 <= overlap_percent < 1:
        raise ValueError("overlap_percent must be between 0 and 1")

    model = get_model()
    tokenizer = model.tokenizer

    # Reserve space for special tokens
    max_tokens = (
        model.max_seq_length 
        - tokenizer.num_special_tokens_to_add(pair=False)
    )

    if chunk_size is None:
        chunk_size = int(max_tokens * 0.80)
    

    token_ids = tokenizer.encode(
        text,
        add_special_tokens=False,
        truncation=False,
        verbose=False
    )

    overlap = int(chunk_size * overlap_percent)
    step = chunk_size - overlap

    chunks = []

    for start in range(0, len(token_ids), step):
        chunk_ids = token_ids[start:start + chunk_size]

        if not chunk_ids:
            break

        chunk = tokenizer.decode(
            chunk_ids,
            skip_special_tokens=True
        )

        chunks.append(chunk)

        if start + chunk_size >= len(token_ids):
            break

    return chunks