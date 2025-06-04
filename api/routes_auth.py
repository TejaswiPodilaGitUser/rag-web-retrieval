# api/routes_auth.py

from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv
from pathlib import Path
# api/routes_auth.py
# Import necessary libraries
# ✅ Load .env explicitly from project root
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
print(f"🔍 Loading .env from: {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)

API_KEY = os.getenv("SECRET_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    print(f"🔐 Provided API key: {x_api_key}")
    print(f"🔑 Expected API key: {API_KEY}")
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="❌ Invalid or missing API key."
        )
