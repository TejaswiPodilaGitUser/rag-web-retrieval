import streamlit as st
import requests
from chat_fallback import get_fallback_response, SAMPLE_CONVERSATIONS, normalize_text
from rag_engine import fetch_rag_response

def show_chat():
    st.header("💬 Chat with our AI Bot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_area("Enter your message:", key="user_input")
    send_clicked = st.button("Send")

    if send_clicked:
        if user_input.strip():
            user_text = user_input.strip()
            st.session_state.messages.append({"role": "user", "content": user_text})

            # Check sample responses first
            normalized_input = normalize_text(user_text)
            sample_response = next(
                (conv["bot"] for conv in SAMPLE_CONVERSATIONS if normalize_text(conv["user"]) == normalized_input),
                None
            )

            if sample_response:
                response = sample_response
            else:
                # Try RAG response
                try:
                    rag_data = fetch_rag_response(
                        query=user_text,
                        top_k=3,
                        min_score=0.0,
                        save_to_csv=False
                    )
                    answer = rag_data.get("answer", "")
                    response = answer.strip() if isinstance(answer, str) else answer.get("content", "").strip()
                except Exception:
                    response = None

                # Use fallback if RAG is not confident
                if not response or any(x in response.lower() for x in [
                    "something went wrong", "based on the information found", "i'm sorry", "can't find", "don't know",
                    "no relevant documents"
                ]):
                    response = get_fallback_response(user_text)

            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.warning("⚠️ Please enter a message.")

    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 Bot:** {msg['content']}")

    # Feedback Section
    if st.session_state.messages:
        st.subheader("📝 Provide Feedback")
        feedback_text = st.text_input("What do you think about the response?")
        feedback_rating = st.slider("Rate the response (1 = Poor, 5 = Excellent)", 1, 5, 3)

        if st.button("Submit Feedback"):
            last_user = next((msg["content"] for msg in reversed(st.session_state.messages) if msg["role"] == "user"), "")
            last_bot = next((msg["content"] for msg in reversed(st.session_state.messages) if msg["role"] == "assistant"), "")

            feedback_payload = {
                "user_input": last_user,
                "bot_response": last_bot,
                "rating": feedback_rating,
                "feedback": feedback_text
            }

            try:
                feedback_res = requests.post(
                    "http://localhost:8000/api/feedback",
                    json=feedback_payload,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": "my-super-secret-key"
                    }
                )
                if feedback_res.status_code == 200:
                    st.success("✅ Feedback submitted successfully!")
                else:
                    st.error("❌ Failed to submit feedback.")
            except Exception as e:
                st.error(f"❌ Error submitting feedback: {e}")
