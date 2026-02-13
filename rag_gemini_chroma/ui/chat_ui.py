import streamlit as st
import requests

st.title("💬 RAG Chat")

question = st.text_input("Ask a question")

if question:
    response = requests.post(
        "http://localhost:8000/query",
        params={"question": question}
    )
    st.write(response.json()["answer"])
