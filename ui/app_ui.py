import streamlit as st
import requests
import json

# Title of the app
st.title("AI-Powered Chatbot and Query Interface")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ("Home", "Chat", "Query"))

# Home Page
if page == "Home":
    st.header("Welcome to the AI-Powered Chatbot and Query Interface")
    st.write(
        """
        This application allows you to interact with our AI-powered system for chatting and querying purposes.
        You can use the chatbot to converse and ask questions or submit a query for detailed responses.
        """
    )

# Chat Page
elif page == "Chat":
    st.header("Chat with our AI Bot")

    user_input = st.text_area("Enter your message:", "")
    
    if st.button("Send"):
        if user_input:
            # Send the user input to the API endpoint (assume an endpoint exists at `/chat`)
            payload = json.dumps({"message": user_input})
            response = requests.post("http://localhost:8000/api/chat", data=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                bot_response = response.json()["response"]
                st.write(f"**Bot**: {bot_response}")
            else:
                st.write("Error: Something went wrong with the API.")
        else:
            st.write("Please enter a message.")

# Query Page
elif page == "Query":
    st.header("Submit a Query")

    query_input = st.text_area("Enter your query:", "")
    
    if st.button("Submit Query"):
        if query_input:
            # Send the query input to the API endpoint (assume an endpoint exists at `/query`)
            payload = json.dumps({"query": query_input})
            response = requests.post("http://localhost:8000/api/query", data=payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                query_result = response.json()["result"]
                st.write(f"**Result**: {query_result}")
            else:
                st.write("Error: Something went wrong with the API.")
        else:
            st.write("Please enter a query.")
