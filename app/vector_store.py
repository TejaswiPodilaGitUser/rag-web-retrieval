import faiss
import numpy as np
import pandas as pd
import json
import os
from typing import List, Dict, Union, Optional

class VectorStore:
    def __init__(self, dim: int, use_cosine: bool = True,
                 index_path="outputs/index.faiss",
                 meta_path="outputs/metadata.json"):
        """
        Initialize the VectorStore with FAISS index and metadata.

        Args:
            dim (int): Dimensionality of embeddings.
            use_cosine (bool): Whether to use cosine similarity (default True).
            index_path (str): Path to save/load the FAISS index.
            meta_path (str): Path to save/load the metadata.
        """
        self.dim = dim
        self.use_cosine = use_cosine
        self.index_path = index_path
        self.meta_path = meta_path

        self.index = faiss.IndexFlatIP(dim) if use_cosine else faiss.IndexFlatL2(dim)
        self.metadata: List[Dict] = []

        self._load()

    def _normalize(self, embeddings: np.ndarray) -> np.ndarray:
        """Normalize vectors for cosine similarity."""
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1  # avoid division by zero
        return embeddings / norms

    def add(self, embeddings: Union[np.ndarray, List], meta: List[Dict]):
        """Add embeddings and associated metadata."""
        embeddings = np.array(embeddings, dtype='float32')
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        elif embeddings.ndim != 2:
            raise ValueError(f"Invalid embedding shape: {embeddings.shape}")

        if len(embeddings) != len(meta):
            raise ValueError("Embeddings and metadata count mismatch.")

        if self.use_cosine:
            embeddings = self._normalize(embeddings)

        self.index.add(embeddings)
        self.metadata.extend(meta)
        self._save()

    def add_documents(self, docs: List[Dict]):
        """
        Add a list of documents. Each must have an 'embedding' and 'text'.
        """
        embeddings = [doc["embedding"] for doc in docs]
        meta = [{"text": doc["text"], "url": doc.get("url", "")} for doc in docs]
        self.add(embeddings, meta)
        print(f"✅ Added {len(embeddings)} documents. Total in index: {self.index.ntotal}")

    def search(self, query_embedding: Union[np.ndarray, List], top_k: int = 5, min_score: Optional[float] = None) -> List[Dict]:
        """
        Search for the top_k most similar vectors to the query_embedding.

        Args:
            query_embedding (np.ndarray or list): Query vector.
            top_k (int): Number of top results to return.
            min_score (float): Optional minimum score filter.

        Returns:
            List[Dict]: Search results with scores and metadata.
        """
        print("🔍 Searching FAISS index...")
        if self.index.ntotal == 0:
            print("⚠️ No documents in index.")
            return []

        query_embedding = np.array(query_embedding, dtype='float32').reshape(1, -1)

        if query_embedding.shape[1] != self.dim:
            raise ValueError(f"Query dimension mismatch: expected {self.dim}, got {query_embedding.shape[1]}")

        if self.use_cosine:
            query_embedding = self._normalize(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if 0 <= idx < len(self.metadata):
                if min_score is None or score >= min_score:
                    result = self.metadata[idx].copy()
                    result["score"] = float(score)
                    results.append(result)

        print(f"📌 Retrieved {len(results)} results.")
        return results

    def search_to_csv(self, query_embedding: Union[np.ndarray, List], path: str, top_k: int = 5):
        """
        Perform a search and save the results to a CSV.

        Args:
            query_embedding (np.ndarray or list): Query vector.
            path (str): Path to save the CSV file.
            top_k (int): Number of top results.
        """
        results = self.search(query_embedding, top_k=top_k)
        df = pd.DataFrame(results)
        df.to_csv(path, index=False)
        print(f"📄 Results saved to: {path}")

    def _save(self):
        """Save FAISS index and metadata to disk."""
        # Create parent directory for index_path, if any
        index_dir = os.path.dirname(self.index_path)
        if index_dir:
            os.makedirs(index_dir, exist_ok=True)

        # Create parent directory for meta_path, if any
        meta_dir = os.path.dirname(self.meta_path)
        if meta_dir:
            os.makedirs(meta_dir, exist_ok=True)

        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)


    def _load(self):
        """Load FAISS index and metadata from disk."""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            print(f"📥 Loaded FAISS index from {self.index_path}")
        if os.path.exists(self.meta_path):
            with open(self.meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
            print(f"📥 Loaded metadata from {self.meta_path}")

    def reset(self):
        """Reset the index and metadata, and delete associated files."""
        self.index = faiss.IndexFlatIP(self.dim) if self.use_cosine else faiss.IndexFlatL2(self.dim)
        self.metadata = []
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
        if os.path.exists(self.meta_path):
            os.remove(self.meta_path)
        print("🧹 Vector store reset completed.")

# Singleton instance
_vector_store_instance: Optional[VectorStore] = None

def get_vector_store() -> VectorStore:
    """
    Returns a singleton instance of VectorStore with predefined settings.
    """
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore(dim=384, use_cosine=True)
    return _vector_store_instance
