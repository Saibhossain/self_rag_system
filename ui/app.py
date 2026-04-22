import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="Self-RAG Chat", layout="wide")

st.title("🤖 Self-RAG Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input
prompt = st.chat_input("Ask something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Call API
    response = requests.post(API_URL, json={"question": prompt})
    answer = response.json()["answer"]

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
