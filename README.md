# 🧠 AI Chatbot with Citations and Feedback

This project is an AI-powered chatbot that allows users to have natural language conversations with an assistant, view source citations, and provide feedback on responses. It features a Streamlit frontend and a FastAPI backend.

---

## 🚀 Features

- ✅ Chat with an AI assistant in real-time
- 🔗 Automatically displays source citations for transparency
- 📝 Allows user feedback with rating and comments
- ⚙️ Streamlit frontend with interactive UI
- 🚀 FastAPI backend for API and processing
- 🔍 Debug info panel for testing API responses

---

## 📁 Project Structure
```bash
ai-chat-app/
│
├── frontend/
│ └── app.py # Streamlit frontend for chat interface
│
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── models.py # Pydantic models for request/response
│ ├── router.py # Route logic for /chat and /feedback
│ ├── engine.py # Core logic to generate AI responses
│ └── feedback_store.py # (Optional) Feedback persistence logic
│
├── requirements.txt # Required Python packages
└── README.md # This file
```

---

## 🛠️ Installation & Setup

### 🔧 Backend (FastAPI)

1. Go to the backend directory:
```bash
cd backend
```
- Set up a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Run the FastAPI app:
```bash
uvicorn main:app --reload --port 8000
Access API docs at:
http://localhost:8000/docs
```
### 💻 Frontend (Streamlit)
Go to the frontend directory:
```bash
cd frontend
Install required libraries:

pip install -r requirements.txt
```
### Start the Streamlit app:
```bash
streamlit run app.py
```

###  🔄 API Overview
- 🗨️ POST /api/v1/chat
- Sends a message to the chatbot and receives a response.

### Request:
```bash
{
  "messages": [
    { "role": "user", "content": "What is artificial intelligence?" }
  ]
}
```
### Response:
```bash
{
  "answer": {
    "content": "Artificial Intelligence (AI) refers to..."
  },
  "citations": [
    {
      "text": "Stanford AI Definition",
      "url": "https://example.com/ai"
    }
  ]
}
```
### 📝 POST /api/feedback
Saves user feedback and rating on a given response.
```bash
Request:
{
  "user_input": "What is AI?",
  "bot_response": "AI is...",
  "rating": 5,
  "feedback": "Very helpful!"
}
```
### Response:
```bash
{
  "message": "Feedback received"
}
```
### 🧪 Example Workflow
- User types a message like "Tell me about machine learning."

- Bot responds with an informative answer.

- The user views citation links for source material.

- User submits a rating and feedback for future improvements.

### 🧰 Tech Stack
- Python 3.9+

- FastAPI for API backend

- Streamlit for chat frontend

- Pydantic for schema validation

- Requests for HTTP communication

- Optional: OpenAI / LangChain for response generation

### 📌 Future Improvements
- Add support for PDF/CSV document uploads

- Store chat history per user

- Authenticate users via login

- Integrate vector search with FAISS

- Enhance feedback analytics

