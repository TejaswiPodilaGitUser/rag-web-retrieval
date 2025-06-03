import sys
import os
from typing import List
from app.scraper import scrape_text_from_url
from app.chunker import chunk_text
from app.embedder import get_embedding_local
from app.vector_store import get_vector_store

# Optional: set the project root for imports if running standalone
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def index_urls(urls: List[str]) -> dict:
    vector_db = get_vector_store()
    indexed = []
    failed = []

    for url in urls:
        try:
            print(f"📥 Starting scrape for URL: {url}")
            content = scrape_text_from_url(url)

            if not content:
                print(f"⚠️ Empty content for URL: {url}")
                failed.append({"url": url, "reason": "Empty content"})
                continue

            chunks = chunk_text(content)
            print(f"🧩 Split content into {len(chunks)} chunks")

            embeddings = []
            metadata = []

            for chunk in chunks:
                emb = get_embedding_local(chunk)
                if emb is not None:
                    embeddings.append(emb)
                    metadata.append({"url": url, "text": chunk})
                else:
                    print(f"⚠️ Failed to get embedding for chunk: {chunk[:50]}...")

            if embeddings:
                vector_db.add(embeddings, metadata)
                print(f"✅ Added {len(embeddings)} embeddings for URL: {url}")
                print(f"📌 Total vectors in index: {vector_db.index.ntotal}")
                indexed.append(url)
            else:
                print(f"⚠️ No embeddings generated for URL: {url}")
                failed.append({"url": url, "reason": "No embeddings generated"})

        except Exception as e:
            print(f"❌ Exception processing URL {url}: {e}")
            failed.append({"url": url, "reason": str(e)})

    return {"status": "success", "indexed_urls": indexed, "failed": failed}

if __name__ == "__main__":
    # Example URLs to index (replace or extend this list)
    urls_to_index = [
        "https://en.wikipedia.org/wiki/ColBERT",
        "https://en.wikipedia.org/wiki/Faiss",
        # Add more URLs as needed
    ]

    result = index_urls(urls_to_index)
    print("\nIndexing summary:")
    print(result)
