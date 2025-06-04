# rag_engine.py

import requests
import json

def fetch_rag_response(query: str, top_k: int = 5, min_score: float = 0.0, save_to_csv: bool = False):
    """
    Sends a POST request to the RAG API and returns the parsed response.

    Returns:
        dict: { "answer": str, "citations": list, "csv_path": str or None }
    """
    payload = {
        "query": query,
        "top_k": top_k,
        "min_score": min_score,
        "save_to_csv": save_to_csv
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": "my-super-secret-key"  # Update if needed
    }

    try:
        response = requests.post(
            "http://localhost:8000/api/query",
            data=json.dumps(payload),
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"API Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Connection error: {e}")
