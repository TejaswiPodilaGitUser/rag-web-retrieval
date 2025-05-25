# api/routes_index.py
from fastapi import APIRouter, Depends
from app.scraper import scrape_text_from_url
from app.chunker import chunk_text
from app.embedder import get_embedding_local
from app.vector_store import get_vector_store
from app.auth import get_current_user

router = APIRouter()

@router.post("/api/v1/index")
def index_url(data: dict, user: str = Depends(get_current_user)):
    urls = data.get("url", [])
    vector_db = get_vector_store()
    indexed = []
    failed = []

    for url in urls:
        try:
            content = scrape_text_from_url(url)
            if not content:
                failed.append({"url": url, "reason": "Empty content"})
                continue

            chunks = chunk_text(content)
            embeddings = []
            metadata = []

            for chunk in chunks:
                emb = get_embedding_local(chunk)
                if emb is not None:
                    embeddings.append(emb)
                    metadata.append({"url": url, "text": chunk})

            if embeddings:
                vector_db.add(embeddings, metadata)
                indexed.append(url)
            else:
                failed.append({"url": url, "reason": "No embeddings generated"})

        except Exception as e:
            failed.append({"url": url, "reason": str(e)})

    return {"status": "success", "indexed_url": indexed, "failed": failed}
