import streamlit as st
import requests
import json
import re

def show_query():
    st.header("🔍 Submit a Query")

    # Initialize session state variables if not present
    if "query_submitted" not in st.session_state:
        st.session_state.query_submitted = False
    if "top_k" not in st.session_state:
        st.session_state.top_k = 5
    if "min_score" not in st.session_state:
        st.session_state.min_score = 0.0
    if "save_csv" not in st.session_state:
        st.session_state.save_csv = False

    # Initialize result storage variables
    if "last_answer" not in st.session_state:
        st.session_state.last_answer = ""
    if "last_citations" not in st.session_state:
        st.session_state.last_citations = []
    if "last_csv_path" not in st.session_state:
        st.session_state.last_csv_path = None

    # Query input and submit button always visible
    query_input = st.text_area("Enter your query:", key="query_input")
    submit = st.button("Submit Query")

    if submit:
        if query_input.strip():
            payload = {
                "query": query_input.strip(),
                "top_k": st.session_state.top_k,
                "min_score": st.session_state.min_score,
                "save_to_csv": st.session_state.save_csv
            }

            try:
                response = requests.post(
                    "http://localhost:8000/api/query",
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    response_json = response.json()

                    raw_result = response_json.get("answer", "No answer found.")
                    cleaned_result = re.sub(r'[,\s]{2,}', ' ', raw_result).strip()

                    # Save results to session state to persist across reruns
                    st.session_state.query_submitted = True
                    st.session_state.last_answer = cleaned_result
                    st.session_state.last_citations = response_json.get("citations", [])
                    st.session_state.last_csv_path = response_json.get("csv_path", None)

                else:
                    st.error("❌ API returned an error.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {e}")
        else:
            st.warning("⚠️ Please enter a query.")

    # Show result from session state if available
    if st.session_state.query_submitted:
        st.markdown("### 📝 Result:")
        st.markdown(st.session_state.last_answer)

        citations = st.session_state.last_citations
        if citations:
            st.markdown("### 🔗 Citations:")
            for i, citation in enumerate(citations, start=1):
                text = citation.get("text", "")[:200].strip()
                url = citation.get("url", None)
                if url:
                    st.markdown(f"{i}. [{text}]({url})")
                else:
                    st.markdown(f"{i}. {text}")

        csv_path = st.session_state.last_csv_path
        if csv_path:
            st.success(f"📄 CSV saved at: `{csv_path}`")
            st.markdown(f"[Download CSV](./{csv_path})")

        # Show sliders and checkbox below results
        st.markdown("---")
        st.subheader("⚙️ Refine Your Query")

        st.session_state.top_k = st.slider(
            "🔢 Top K Results",
            min_value=1,
            max_value=10,
            value=st.session_state.top_k,
            key="top_k_slider"
        )
        st.session_state.min_score = st.slider(
            "🎯 Minimum Score (optional)",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.min_score,
            step=0.01,
            key="min_score_slider"
        )
        st.session_state.save_csv = st.checkbox(
            "💾 Save to CSV",
            value=st.session_state.save_csv,
            key="save_csv_checkbox"
        )

        st.info(f"✅ Selected: Top K = {st.session_state.top_k}, Min Score = {st.session_state.min_score}, Save CSV = {st.session_state.save_csv}")

if __name__ == "__main__":
    show_query()
