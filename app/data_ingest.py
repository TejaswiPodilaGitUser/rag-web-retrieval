import requests
import sys
import os
from bs4 import BeautifulSoup

# Ensure your app directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.vector_store import get_vector_store
from app.embedder import get_embedding_local

# List of source URLs to index
URLS = [
    "https://huyenchip.com/2024/07/25/genai-platform.html",
    "https://lilianweng.github.io/posts/2024-07-07-hallucinatio",
    "https://jina.ai/news/what-is-colbert-and-late-interaction-and-why-they-matter-in-search/",
    "https://quoraengineering.quora.com/Building-Embedding-Search-at-Quora"
]

def fetch_clean_text(url):
    """
    Fetch and clean text content from the given URL using BeautifulSoup.
    """
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)
        return text.strip()
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return ""

def chunk_text(text, max_tokens=300):
    """
    Simple chunking of text into roughly max_tokens character chunks.
    """
    import textwrap
    return textwrap.wrap(text, max_tokens)

def ingest_documents():
    """
    Fetch content, generate embeddings, and add to the vector store.
    """
    vector_store = get_vector_store()
    total_chunks = 0

    for url in URLS:
        print(f"🔍 Fetching: {url}")
        text = fetch_clean_text(url)
        if not text:
            print(f"⚠️ Skipped URL due to empty content: {url}")
            continue

        chunks = chunk_text(text, max_tokens=300)
        docs = []

        for chunk in chunks:
            embedding = get_embedding_local(chunk)
            if embedding is None:
                print("⚠️ Failed to get embedding for a chunk, skipping it.")
                continue

            docs.append({
                "text": chunk,
                "url": url,
                "embedding": embedding
            })

        if docs:
            vector_store.add_documents(docs)
            total_chunks += len(docs)
            print(f"✅ Indexed {len(docs)} chunks from: {url}")
        else:
            print(f"⚠️ No valid embeddings for URL: {url}")

    print(f"🔍 Total indexed chunks: {total_chunks}")
    print(f"📦 FAISS Index size: {vector_store.index.ntotal}")

if __name__ == "__main__":
    ingest_documents()
