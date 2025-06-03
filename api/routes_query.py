from fastapi import APIRouter, Request
from app.vector_store import get_vector_store
from app.embedder import get_embedding_local
import uuid
import os
import re

router = APIRouter()

def extract_summary(docs, max_chars=600):
    """
    Create a short summary by extracting 1–2 sentences per top document.
    """
    summary_parts = []
    total_len = 0
    for doc in docs:
        text = doc.get("text", "").strip()
        if not text:
            continue
        sentences = re.split(r'(?<=[.!?]) +', text)
        snippet = sentences[0] if sentences else text[:200]
        if len(snippet) < 100 and len(sentences) > 1:
            snippet += " " + sentences[1]
        snippet = snippet.strip()
        if snippet not in summary_parts:
            if total_len + len(snippet) > max_chars:
                break
            summary_parts.append(snippet)
            total_len += len(snippet)
    return " ".join(summary_parts)

@router.post("/api/query")
async def query_endpoint(request: Request):
    payload = await request.json()
    query = payload.get("query", "").strip()
    save_to_csv = payload.get("save_to_csv", False)
    top_k = payload.get("top_k", 5)
    min_score = payload.get("min_score", None)

    if not query:
        return {"error": "❌ Query is empty."}

    # Convert min_score to float if provided
    if min_score is not None:
        try:
            min_score = float(min_score)
        except (ValueError, TypeError):
            return {"error": "❌ `min_score` must be a number."}

    # Generate query embedding
    emb = get_embedding_local(query)
    if emb is None or len(emb) == 0:
        return {"error": "❌ Failed to generate embedding."}

    if len(emb.shape) == 1:
        emb = emb.reshape(1, -1)

    # Get vector store
    vector_store = get_vector_store()

    try:
        results = vector_store.search(emb, top_k=top_k, min_score=min_score)
    except TypeError:
        return {
            "error": "❌ Your vector store does not support `min_score`. Please update `vector_store.py`."
        }

    if not results:
        return {"answer": "📝 No relevant documents found.", "citations": []}

    # Sort results by score (descending)
    sorted_results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)

    # Extract short answer summary
    summary = extract_summary(sorted_results[:top_k])
    if not summary:
        summary = "Found documents but could not extract a meaningful summary."

    # Prepare citations list
    citations = [
        {
            "text": doc.get("text", "")[:150].strip(),
            "url": doc.get("url", "")
        }
        for doc in sorted_results[:top_k]
    ]

    # Optional: save to CSV
    csv_path = None
    if save_to_csv:
        os.makedirs("outputs", exist_ok=True)
        filename = f"query_results_{uuid.uuid4().hex[:6]}.csv"
        csv_path = os.path.join("outputs", filename)
        vector_store.search_to_csv(emb, csv_path, top_k=top_k)

    return {
        "query": query,
        "top_k": top_k,
        "min_score": min_score,
        "answer": summary,
        "citations": citations,
        "csv_path": csv_path if save_to_csv else None
    }
