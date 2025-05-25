from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sys
# Append current directory to sys.path
# Append project root to sys.path (one level up from current file)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from api.routes_index import router as index_router
from api.routes_chat import router as chat_router

load_dotenv()

app = FastAPI()

app.include_router(index_router)
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
