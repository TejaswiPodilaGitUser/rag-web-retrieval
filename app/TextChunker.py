# app/chunker.py
from typing import List

class TextChunker:
    def __init__(self, max_words: int = 500, overlap: int = 50):
        """
        Initialize the text chunker.

        Parameters:
        - max_words (int): Maximum number of words per chunk.
        - overlap (int): Number of overlapping words between chunks.
        """
        if overlap >= max_words:
            raise ValueError("Overlap must be smaller than max_words.")
        self.max_words = max_words
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        """
        Chunk the input text into overlapping word-based chunks.

        Parameters:
        - text (str): The text to be chunked.

        Returns:
        - List[str]: List of text chunks.
        """
        words = text.split()
        if len(words) <= self.max_words:
            return [" ".join(words)]

        chunks = []
        step = self.max_words - self.overlap
        for i in range(0, len(words), step):
            chunk = words[i:i + self.max_words]
            chunks.append(" ".join(chunk))
        return chunks


# Optional: simple function-style alias for convenience

def chunk_text(text: str, max_words: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks using the TextChunker class.

    Parameters:
    - text (str): The input text.
    - max_words (int): Maximum number of words per chunk.
    - overlap (int): Number of overlapping words between chunks.

    Returns:
    - List[str]: List of text chunks.
    """
    chunker = TextChunker(max_words=max_words, overlap=overlap)
    return chunker.chunk(text)
