from sentence_transformers import SentenceTransformer

# Load the model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding_local(text):
    """
    Generate embedding using sentence-transformers (runs locally).
    
    Parameters:
    - text (str): The text to embed.

    Returns:
    - list: Embedding vector.
    """
    print(f"🔍 Getting embedding for: {text[:60]}...")
    embedding = model.encode(text)
    print(f"✅ Got embedding of length {len(embedding)}")
    return embedding

# Example
text = "Building A Generative AI Platform"
embedding = get_embedding_local(text)
print(f"Embedding (first 5 values): {embedding[:5]}")
