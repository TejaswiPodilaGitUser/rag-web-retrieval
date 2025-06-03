import os
import sys

# Append project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.TextChunker import chunk_text  # Make sure the function is named this in TextChunker.py

text = "This is a sample document that we want to split into overlapping chunks for semantic search."
chunks = chunk_text(text, max_words=10, overlap=2)  # ✅ Fix the argument name

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}")
