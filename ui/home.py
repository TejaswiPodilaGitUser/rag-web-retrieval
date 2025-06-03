import streamlit as st

def show_home():
    st.header("🏠 Welcome!")
    st.markdown(
        """
        Welcome to the AI-powered chatbot and query interface.  
        Navigate to the **Chat** tab to converse with the AI, or to the **Query** tab to submit custom queries.
        """
    )
