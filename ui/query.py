import streamlit as st
import re
from rag_engine import fetch_rag_response


def initialize_session_state():
    defaults = {
        "query_submitted": False,
        "top_k": 5,
        "min_score": 0.0,
        "save_csv": False,
        "last_answer": "",
        "last_citations": [],
        "last_csv_path": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def handle_query_submission(query_input):
    try:
        response_json = fetch_rag_response(
            query=query_input,
            top_k=st.session_state.top_k,
            min_score=st.session_state.min_score,
            save_to_csv=st.session_state.save_csv
        )
        raw_result = response_json.get("answer", "No answer found.")
        cleaned_result = re.sub(r'[,\s]{2,}', ' ', raw_result).strip()

        st.session_state.query_submitted = True
        st.session_state.last_answer = cleaned_result
        st.session_state.last_citations = response_json.get("citations", [])
        st.session_state.last_csv_path = response_json.get("csv_path", None)

    except (ValueError, ConnectionError) as e:
        st.error(f"❌ {e}")


def display_results():
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


def display_query_controls():
    st.markdown("---")
    st.subheader("⚙️ Refine Your Query")

    st.session_state.top_k = st.slider(
        "🔢 Top K Results",
        min_value=1,
        max_value=5,
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


def show_query():
    st.header("🔍 Submit a Query")
    initialize_session_state()

    query_input = st.text_area("Enter your query:", key="query_input")
    if st.button("Submit Query"):
        if query_input.strip():
            handle_query_submission(query_input.strip())
        else:
            st.warning("⚠️ Please enter a query.")

    if st.session_state.query_submitted:
        display_results()
        display_query_controls()


if __name__ == "__main__":
    show_query()
