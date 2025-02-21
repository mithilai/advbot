import os
import streamlit as st
from retriever import retrieve_answer

st.set_page_config(page_title="Advaidh AI Assistant", layout="wide")

st.title("🤖 Advaidh AI Assistant")
st.write("Ask me anything about **Advaidh**, and I'll assist you.")

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("Advaidh", "Hello! How can I help you today?")]

# Display Chat Messages
for role, message in st.session_state.chat_history:
    st.chat_message("user" if role == "You" else "assistant").write(message)

# Chat Input
query = st.chat_input("Ask a question...")
if query:
    with st.spinner("Thinking..."):
        response = retrieve_answer(query)

    # Store Chat History
    st.session_state.chat_history.append(("You", query))
    st.session_state.chat_history.append(("Advaidh", response))

    # Refresh UI
    st.rerun()

# Clear Chat Button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = [("Advaidh", "Hello! How can I help you today?")]
    st.rerun()
