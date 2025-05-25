# api/routes_chat.py
from fastapi import APIRouter, Depends
from app.vector_store import get_vector_store
from app.embedder import get_embedding_local
from app.auth import get_current_user

router = APIRouter()

@router.post("/api/v1/chat")
def chat_endpoint(payload: dict, user: str = Depends(get_current_user)):
    messages = payload.get("messages", [])
    question = messages[-1]["content"]
    vector_store = get_vector_store()
    
    emb = get_embedding_local(question)
    results = vector_store.search(emb)

    if not results:
        return {
            "response": {
                "answer": {"content": "No relevant documents found.", "role": "assistant"},
                "citations": []
            }
        }

    best_match = results[0]
    citations = [{"text": doc["text"][:200], "url": doc["url"]} for doc in results]

    return {
        "response": {
            "answer": {"content": best_match["text"], "role": "assistant"},
            "citations": citations
        }
    }
