import streamlit as st
import requests

API_URL = "http://api:8000/chat"
UPLOAD_URL = "http://api:8000/upload"

st.title("RAG Chat Assistant")
st.caption("Ask questions about your documents")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()

# Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Upload area — compact, just above the chat input
uploaded_file = st.file_uploader("➕ Add a document", type=["pdf"], label_visibility="collapsed")

if uploaded_file is not None and uploaded_file.name not in st.session_state.indexed_files:
    with st.spinner(f"Indexing {uploaded_file.name}..."):
        response = requests.post(
            UPLOAD_URL,
            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        )
    if response.status_code == 200:
        st.session_state.indexed_files.add(uploaded_file.name)
        st.success(response.json()["message"])
    else:
        st.error(f"Error: {response.json().get('detail', 'Upload failed')}")

# Chat input
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            response = requests.post(API_URL, json={"question": prompt})
            data = response.json()
            answer = data["answer"]
            sources = data["sources"]
        st.write(answer)
        st.caption(f"Sources: {', '.join(sources)}")
        st.session_state.messages.append({"role": "assistant", "content": answer})
