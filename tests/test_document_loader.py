import os
import sys

# Append project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.DocumentLoader import DocumentLoader


if __name__ == "__main__":
    loader = DocumentLoader("data/documents")
    docs = loader.load_documents()

    for doc in docs:
        print(doc["filename"])
        print(doc["content"][:200])  # preview
