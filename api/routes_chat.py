# routes_chat.py

from fastapi import APIRouter, Depends
from app.vector_store import get_vector_store
from app.embedder import get_embedding_local
from .routes_auth import verify_api_key  # import auth dependency
import traceback
import re

router = APIRouter()

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

@router.post("/api/v1/chat", dependencies=[Depends(verify_api_key)])
def chat_endpoint(payload: dict):
    try:
        messages = payload.get("messages", [])
        if not messages or not isinstance(messages, list):
            return {
                "response": {
                    "answer": {"content": "No question provided.", "role": "assistant"},
                    "citations": []
                }
            }

        question = messages[-1].get("content", "").strip()
        if not question:
            return {
                "response": {
                    "answer": {"content": "Empty question received.", "role": "assistant"},
                    "citations": []
                }
            }

        print(f"🔍 Getting embedding for: {question}...")
        vector_store = get_vector_store()
        emb = get_embedding_local(question)
        print(f"✅ Got embedding of length {len(emb)}")

        print("🔍 Searching FAISS index...")
        results = vector_store.search(emb)
        print(f"📌 Retrieved {len(results)} results.")

        if not results:
            return {
                "response": {
                    "answer": {"content": "No relevant documents found.", "role": "assistant"},
                    "citations": []
                }
            }

        sorted_results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)

        summary = extract_summary(sorted_results[:3])
        if not summary:
            summary = "I found documents but couldn't extract a meaningful summary."

        answer_text = f"Based on the information found in the documents, here is a summary:\n\n{summary}"

        citations = [
            {
                "text": doc.get("text", "")[:150].strip(),
                "url": doc.get("url", "")
            } for doc in sorted_results[:3]
        ]

        return {
            "response": {
                "answer": {
                    "content": answer_text,
                    "role": "assistant"
                },
                "citations": citations
            }
        }

    except Exception:
        print("❌ Error in chat_endpoint:\n", traceback.format_exc())
        return {
            "response": {
                "answer": {
                    "content": "Something went wrong. Please try again later.",
                    "role": "assistant"
                },
                "citations": []
            }
        }
