import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/upload"

st.set_page_config(page_title="PDF Upload", page_icon="📄")
st.title("📄 Upload PDF for RAG")

uploaded_file = st.file_uploader(
    "Select a PDF file",
    type=["pdf"],
    accept_multiple_files=False
)

upload_clicked = st.button("⬆️ Upload PDF")

if upload_clicked:
    if uploaded_file is None:
        st.warning("Please select a PDF before clicking Upload.")
    else:
        with st.spinner("Uploading and processing PDF..."):
            try:
                response = requests.post(
                    API_URL,
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            "application/pdf"
                        )
                    },
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(data.get("status", "PDF uploaded successfully"))
                else:
                    st.error(f"Upload failed (status {response.status_code})")
                    st.text(response.text)

            except Exception as e:
                st.error("Failed to connect to backend API")
                st.text(str(e))
