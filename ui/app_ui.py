import streamlit as st
from home import show_home
from chat import show_chat
from query import show_query

st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("🤖 AI-Powered Chatbot and Query Interface")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ("Home", "Chat", "Query"))

# Route to the selected page
if page == "Home":
    show_home()
elif page == "Chat":
    show_chat()
elif page == "Query":
    show_query()
