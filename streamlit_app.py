import streamlit as st
import requests

API_URL = "http://api:8000/chat"

st.title("RAG Chat Assistant")
st.caption("Ask questions about your documents")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

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