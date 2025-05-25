# app/retriever.py
def retrieve(query, vector_store, k=5):
    return vector_store.similarity_search(query, k=k)
