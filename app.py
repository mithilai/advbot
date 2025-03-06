import os
import streamlit as st
import requests  # Import requests to call the FastAPI backend

st.set_page_config(page_title="Advaidh AI Assistant", layout="wide")

st.title("🤖 Advaidh AI Assistant")
st.write("Ask me anything about **Advaidh**, and I'll assist you.")

# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000/chat"

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("Advaidh", "Hello! How can I help you today?")]

# Display Chat Messages
for role, message in st.session_state.chat_history:
    st.chat_message("user" if role == "You" else "assistant").write(message)


query = st.chat_input("Ask a question...")
if query:
    with st.spinner("Thinking..."):
        print(f"Sending request to API: {query}")  # Debugging print
        response = requests.post(API_URL, json={"message": query})
    
    print(f"Received response: {response.status_code}")  # Debugging print

    if response.status_code == 200:
        bot_response = response.json().get("response", "I am unable to answer right now!")
    else:
        bot_response = f"Error: Unable to fetch response ({response.status_code})"

    st.session_state.chat_history.append(("You", query))
    st.session_state.chat_history.append(("Advaidh", bot_response))
    st.rerun()

# # Chat Input
# query = st.chat_input("Ask a question...")
# if query:
#     with st.spinner("Thinking..."):
#         response = requests.post(API_URL, json={"message": query})
    
#     if response.status_code == 200:
#         bot_response = response.json().get("response", "I am unable to answer right now!")
#     else:
#         bot_response = "Error: Unable to fetch response from the chatbot."

#     # Store Chat History
#     st.session_state.chat_history.append(("You", query))
#     st.session_state.chat_history.append(("Advaidh", bot_response))

#     # Refresh UI
#     st.rerun()

# Clear Chat Button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = [("Advaidh", "Hello! How can I help you today?")]
    st.rerun()
