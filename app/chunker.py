def chunk_text(text, max_tokens=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens - overlap):
        chunk = words[i:i + max_tokens]
        chunks.append(" ".join(chunk))
    return chunks
