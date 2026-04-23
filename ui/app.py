import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000/ask"

st.set_page_config(
    page_title="Self-RAG Chat",
    layout="wide",
    page_icon="🤖"
)

if "conversations" not in st.session_state:
    st.session_state.conversations = {}
    
if "thread_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.thread_id = new_id
    st.session_state.conversations[new_id] = []


# ===================== SIDEBAR =====================
with st.sidebar:
    st.title("⚙️ Settings")

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    st.markdown(f"**Session ID:** `{st.session_state.thread_id[:8]}`")

    if st.button("🧹 Clear Current Chat"):
        st.session_state.conversations[st.session_state.thread_id] = []
        st.rerun()
        
    st.title("💬 Conversations")

    # List all conversations
    for tid, msgs in st.session_state.conversations.items():
        # Use first message as title
        title = msgs[0]["content"][:30] + "..." if msgs else "New Chat"

        if st.button(title, key=tid):
            st.session_state.thread_id = tid
            st.rerun()

    st.divider()
    
    
     # New chat button
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.thread_id = new_id
        st.session_state.conversations[new_id] = []
        st.rerun()
        

    st.subheader("🔍 Debug")
    show_debug = st.toggle("Show debug info", value=False)

# ===================== MAIN =====================

st.title("🤖 Self-RAG Chat")
st.caption("Ask questions over your documents with intelligent retrieval")


current_thread = st.session_state.thread_id

if current_thread not in st.session_state.conversations:
    st.session_state.conversations[current_thread] = []

st.session_state.messages = st.session_state.conversations[current_thread]


# ===================== CHAT DISPLAY =====================

chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ===================== INPUT =====================

prompt = st.chat_input("Ask something about your documents...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "assistant", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # ===================== API CALL =====================
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):

            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": prompt,
                        "thread_id": st.session_state.thread_id
                    },
                    timeout=60
                )

                data = response.json()

                answer = data.get("answer", "⚠️ No response")
                debug_info = data.get("debug", {})

            except Exception as e:
                answer = f"❌ Error: {str(e)}"
                debug_info = {}

        # Show answer
        st.markdown(answer)

        # ===================== DEBUG PANEL =====================
        if show_debug and debug_info:
            with st.expander("🔍 Debug Info"):
                st.json(debug_info)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
