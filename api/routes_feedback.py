# api/routes_feedback.py
from fastapi import APIRouter, Request
import json

router = APIRouter()

@router.post("/api/feedback")
async def submit_feedback(request: Request):
    data = await request.json()
    with open("feedback_log.jsonl", "a") as f:
        f.write(json.dumps(data) + "\n")
    return {"message": "Feedback submitted successfully"}
