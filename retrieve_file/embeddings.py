from functools import lru_cache

@lru_cache(maxsize=1)
def get_model():
    from sentence_transformers import SentenceTransformer   # Embedding model
    return SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text):
    model = get_model()
    return model.encode(text)

if __name__ == "__main__":
    text = "Veterinary clinic management system"

    embedding = generate_embedding(text)

    print("Vector dimension:", len(embedding))
    print("Vector shape:", embedding.shape)
    print("First 5 values:", embedding[:5])
