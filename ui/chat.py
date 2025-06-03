import streamlit as st
import requests
import json

def show_chat():
    st.header("💬 Chat with our AI Bot")
    user_input = st.text_area("Enter your message:")

    if st.button("Send"):
        if user_input.strip():
            payload = json.dumps({
                "messages": [{"role": "user", "content": user_input.strip()}]
            })

            try:
                response = requests.post(
                    "http://localhost:8000/api/v1/chat",
                    data=payload,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    full_response = response.json()

                    # Show entire raw response for debugging
                    with st.expander("🧪 API Debug Info", expanded=False):
                        st.json(full_response)

                    result = full_response.get("response", {})

                    # Extract and handle bot response
                    answer = result.get("answer", {})
                    if isinstance(answer, dict):
                        bot_response = answer.get("content", "").strip()
                    elif isinstance(answer, str):
                        bot_response = answer.strip()
                    else:
                        bot_response = ""

                    if not bot_response:
                        st.warning("⚠️ No valid response received from the bot. Please try again.")
                    else:
                        st.markdown(f"**🧠 Bot:** {bot_response}")

                    # Extract and show citations
                    citations = result.get("citations", [])
                    cleaned_citations = []
                    seen_texts = set()

                    for citation in citations:
                        text = citation.get("text", "").strip()
                        url = citation.get("url", None)

                        # Skip invalid or repeated text
                        if not text or "something went wrong" in text.lower() or text in seen_texts:
                            continue
                        seen_texts.add(text)
                        cleaned_citations.append((text[:200], url))

                    if cleaned_citations:
                        st.subheader("🔗 Citations")
                        for i, (text, url) in enumerate(cleaned_citations, start=1):
                            if url:
                                st.markdown(f"{i}. [{text}]({url})")
                            else:
                                st.markdown(f"{i}. {text}")
                    else:
                        st.info("ℹ️ No valid citations available.")

                    # Feedback section
                    st.subheader("📝 Provide Feedback")
                    feedback_text = st.text_input("What do you think about the response?")
                    feedback_rating = st.slider("Rate the response (1 = Poor, 5 = Excellent)", 1, 5, 3)

                    if st.button("Submit Feedback"):
                        feedback_payload = {
                            "user_input": user_input,
                            "bot_response": bot_response,
                            "rating": feedback_rating,
                            "feedback": feedback_text
                        }

                        try:
                            feedback_res = requests.post(
                                "http://localhost:8000/api/feedback",
                                data=json.dumps(feedback_payload),
                                headers={"Content-Type": "application/json"}
                            )
                            if feedback_res.status_code == 200:
                                st.success("✅ Feedback submitted successfully!")
                            else:
                                st.error("❌ Failed to submit feedback.")
                        except Exception as e:
                            st.error(f"❌ Error submitting feedback: {e}")

                else:
                    st.error(f"❌ API returned error code {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {e}")
        else:
            st.warning("⚠️ Please enter a message.")
