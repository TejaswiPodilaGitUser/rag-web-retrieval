from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(Path(__file__).resolve().parent.parent, ".env"))

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Import routers
from api.routes_index import router as index_router
from api.routes_chat import router as chat_router
from api.routes_feedback import router as feedback_router
from api.routes_query import router as query_router

# Import VectorStore loader
from app.vector_store import get_vector_store

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: load FAISS index
    vector_store = get_vector_store()
    vector_store._load()
    print(f"📦 FAISS index loaded at startup with {vector_store.index.ntotal} vectors")
    yield
    print("🛑 Shutting down FastAPI app...")

# ✅ Final app instantiation (only once)
app = FastAPI(
    title="AI Search Backend",
    version="1.0",
    description="FastAPI backend for semantic search and chat with feedback.",
    lifespan=lifespan
)

# ✅ Include API routers
app.include_router(index_router)
app.include_router(chat_router)
app.include_router(feedback_router)
app.include_router(query_router)

# ✅ Root endpoint
@app.get("/")
def read_root():
    return {"message": "🚀 Hello, World! The backend is running."}
