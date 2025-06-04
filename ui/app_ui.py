import streamlit as st
from home import show_home
from chat import show_chat
from query import show_query

st.set_page_config(page_title="AI Chatbot", layout="wide")

# Center the title using columns
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title("🤖 AI-Powered Chatbot and Query Interface")

# Center tabs the same way
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    tab1, tab2, tab3 = st.tabs(["🏠 Home", "💬 Chat", "🔍 Query"])

    with tab1:
        show_home()

    with tab2:
        show_chat()

    with tab3:
        show_query()
