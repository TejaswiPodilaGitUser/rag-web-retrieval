from fastapi import APIRouter, Request
from app.vector_store import get_vector_store
from app.embedder import get_embedding_local
import uuid
import os
import re
import difflib

router = APIRouter()

GENERIC_FALLBACK = (
    "🤖 I'm here to assist with queries related to the indexed topics. "
    "It seems your question doesn't match the available content. "
    "Please rephrase or try asking about GenAI platforms, ColBERT, hallucinations, embedding search, vector databases, or similar AI topics."
)

def extract_summary(docs, max_chars=600):
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

def highlight_snippet(doc_text, query, max_len=180):
    sentences = re.split(r'(?<=[.!?]) +', doc_text.strip())
    if not sentences:
        return ""
    best_match = max(
        sentences,
        key=lambda s: difflib.SequenceMatcher(None, s.lower(), query.lower()).ratio(),
        default=""
    )
    snippet = best_match
    try:
        idx = sentences.index(best_match)
        if len(best_match) < 50 and idx + 1 < len(sentences):
            snippet += " " + sentences[idx + 1]
    except ValueError:
        pass
    return snippet[:max_len].strip()

def clean_text_fragment(text):
    text = text.strip()
    if text and text[-1] not in ".!?":
        last_punc = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
        if last_punc != -1:
            return text[:last_punc + 1]
    return text

def is_stupid_query(query):
    """
    Heuristic check for invalid or nonsense queries.
    """
    lowered = query.lower()
    offensive_words = ["stupid", "nonsense", "idiot", "dumb", "what is this", "nonsense answer"]
    return any(bad in lowered for bad in offensive_words) or len(query.split()) <= 2

@router.post("/api/query")
async def query_endpoint(request: Request):
    payload = await request.json()
    query = payload.get("query", "").strip()
    save_to_csv = payload.get("save_to_csv", False)
    top_k = payload.get("top_k", 5)
    min_score = payload.get("min_score", None)

    if not query:
        return {"error": "❌ Query is empty."}

    if is_stupid_query(query):
        return {"answer": GENERIC_FALLBACK, "citations": []}

    if min_score is not None:
        try:
            min_score = float(min_score)
        except (ValueError, TypeError):
            return {"error": "❌ `min_score` must be a number."}

    emb = get_embedding_local(query)
    if emb is None or len(emb) == 0:
        return {"error": "❌ Failed to generate embedding."}

    if len(emb.shape) == 1:
        emb = emb.reshape(1, -1)

    vector_store = get_vector_store()

    try:
        results = vector_store.search(emb, top_k=top_k, min_score=min_score)
    except TypeError:
        return {
            "error": "❌ Your vector store does not support `min_score`. Please update `vector_store.py`."
        }

    if not results:
        return {"answer": "📝 No relevant documents found.", "citations": []}

    sorted_results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)
    score_threshold = 0.6
    filtered_results = [doc for doc in sorted_results if doc.get("score", 0) >= score_threshold]

    if not filtered_results:
        return {"answer": "📝 No relevant documents found with sufficient relevance.", "citations": []}

    sorted_results = filtered_results

    summary = extract_summary(sorted_results[:top_k])
    summary = clean_text_fragment(summary)
    if not summary:
        summary = "Found documents but could not extract a meaningful summary."

    citations = []
    for doc in sorted_results[:top_k]:
        snippet = highlight_snippet(doc.get("text", ""), query)
        snippet = clean_text_fragment(snippet)
        citations.append({
            "text": snippet,
            "url": doc.get("url", "")
        })

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
