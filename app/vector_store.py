import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int):
        """
        Initialize the FAISS index and metadata storage.

        Parameters:
        - dim (int): Dimensionality of the embeddings (e.g., 384 for MiniLM).
        """
        self.index = faiss.IndexFlatL2(dim)  # L2 distance search index
        self.metadata = []  # Stores metadata associated with each embedding

    def add(self, embeddings, meta):
        """
        Add embeddings and associated metadata to the store.

        Parameters:
        - embeddings (List[List[float]] or np.ndarray): The embedding vectors.
        - meta (List[dict]): Metadata corresponding to each embedding.
        """
        embeddings = np.array(embeddings).astype('float32')

        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        elif embeddings.ndim != 2:
            raise ValueError(f"Invalid embedding shape: {embeddings.shape}")

        if len(embeddings) != len(meta):
            raise ValueError(f"Embeddings count ({len(embeddings)}) doesn't match metadata count ({len(meta)})")

        self.index.add(embeddings)
        self.metadata.extend(meta)

    def search(self, query_embedding, top_k=5):
        """
        Perform similarity search for a query embedding.

        Parameters:
        - query_embedding (List[float] or np.ndarray): The query embedding.
        - top_k (int): Number of top similar results to return.

        Returns:
        - List[dict]: Metadata of top-k similar entries.
        """
        query_embedding = np.array([query_embedding]).astype('float32')
        _, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results


# Singleton instance
_vector_store_instance = None

def get_vector_store() -> VectorStore:
    """
    Get or create the singleton instance of VectorStore.

    Returns:
    - VectorStore: Global vector store instance.
    """
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore(dim=384)
    return _vector_store_instance
