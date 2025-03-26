import os
import subprocess
import time
import requests
import streamlit as st

# ✅ Set Page Configuration
st.set_page_config(page_title="Advaidh AI Assistant", layout="wide")

# ✅ Start FastAPI as a subprocess
def start_fastapi():
    process = subprocess.Popen(
        ["uvicorn", "api:app", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True  # Added for Windows compatibility
    )
    time.sleep(2)  # Give FastAPI time to start
    # Check if the subprocess is still running
    if process.poll() is None:
        st.sidebar.success("✅ FastAPI backend is running!")
    else:
        st.sidebar.error("❌ Failed to start FastAPI. Check logs.")
        stderr_output, _ = process.communicate()
        st.sidebar.text(stderr_output.decode("utf-8"))
    return process


# ✅ Check if FastAPI is running
try:
    requests.get("http://127.0.0.1:8000/chat")
    fastapi_running = True
except requests.exceptions.ConnectionError:
    fastapi_running = False

# ✅ Start FastAPI if not running
if not fastapi_running:
    fastapi_process = start_fastapi()
    st.sidebar.info("⏳ Starting FastAPI backend...")

# ✅ Streamlit UI
st.title("🤖 Advaidh AI Assistant")
st.write("Ask me anything about **Advaidh**, and I'll assist you.")

API_URL = "http://127.0.0.1:8000/chat"

# ✅ Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("Advaidh", "Hello! How can I help you today?")]

# ✅ Display Chat Messages
for role, message in st.session_state.chat_history:
    st.chat_message("user" if role == "You" else "assistant").write(message)

# ✅ Get the last 3 messages for context
def get_recent_history():
    return st.session_state.chat_history[-3:]  # Get only the last 3 exchanges

query = st.chat_input("Ask a question...")
if query:
    with st.spinner("🤔 Thinking..."):
        history = get_recent_history()
        payload = {"message": query, "history": history}
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        bot_response = response.json().get("response", "⚠️ I am unable to answer right now!")
    else:
        bot_response = f"⚠️ Error: Unable to fetch response ({response.status_code})"

    # ✅ Store Chat History
    st.session_state.chat_history.append(("You", query))
    st.session_state.chat_history.append(("Advaidh", bot_response))
    st.rerun()

# ✅ Clear Chat Button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = [("Advaidh", "Hello! How can I help you today?")]
    st.rerun()
