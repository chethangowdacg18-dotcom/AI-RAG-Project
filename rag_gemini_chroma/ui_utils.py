import base64
import mimetypes
from pathlib import Path
from typing import Any

import requests
import streamlit as st

UPLOAD_API = "http://127.0.0.1:8000/upload"
QUERY_API = "http://127.0.0.1:8000/query"
CHROMA_SUMMARY_API = "http://127.0.0.1:8000/chroma/summary"
CHROMA_CLEAR_API = "http://127.0.0.1:8000/chroma/clear"

ROOT_DIR = Path(__file__).resolve().parent
STYLE_FILE = ROOT_DIR / "static" / "style.css"
LOADER_FILE = ROOT_DIR / "static" / "loader.css"
def ensure_state() -> None:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chroma_loaded" not in st.session_state:
        st.session_state.chroma_loaded = None


def load_css() -> None:
    style_css = STYLE_FILE.read_text(encoding="utf-8")
    loader_css = LOADER_FILE.read_text(encoding="utf-8")
    st.markdown(f"<style>{style_css}\n{loader_css}</style>", unsafe_allow_html=True)


def set_background(image_path: str) -> None:
    path = Path(image_path)
    if not path.exists() or path.stat().st_size == 0:
        st.warning(f"Background image not found: {image_path}")
        return

    mime_type = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")

    st.markdown(
        f"""
        <style>
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stAppViewContainer"] {{
            position: relative;
            overflow: hidden;
        }}

        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed;
            inset: 0;
            z-index: -2;
            background-image: url("data:{mime_type};base64,{b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            filter: none;
            transform: scale(1);
            transition: opacity 0.45s ease-in-out;
        }}

        [data-testid="stAppViewContainer"]::after {{
            content: "";
            position: fixed;
            inset: 0;
            z-index: -1;
            background: linear-gradient(
                145deg,
                rgba(5, 10, 20, 0.68) 0%,
                rgba(8, 14, 28, 0.76) 50%,
                rgba(7, 12, 25, 0.8) 100%
            );
            pointer-events: none;
        }}

        .stApp {{
            color: #f3f7ff !important;
            transition: background 0.45s ease-in-out;
        }}

        p, label, span, div, h1, h2, h3, h4 {{
            color: #ecf4ff;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_loader(text: str = "Loading..."):
    placeholder = st.empty()
    placeholder.markdown(
        f"""
        <div class="rag-loader-overlay">
            <div class="rag-loader-core">
                <span class="rag-ring ring-1"></span>
                <span class="rag-ring ring-2"></span>
                <span class="rag-ring ring-3"></span>
                <div class="rag-loader-text">{text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return placeholder


def sidebar_nav(active: str) -> None:
    with st.sidebar:
        st.markdown("## RAG Menu")
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/embed.py", label="Embed Documents", icon="📄")
        st.page_link("pages/chatbot.py", label="Chatbot", icon="💬")
        st.page_link("pages/chroma_db.py", label="View Chroma DB", icon="🗂️")


def api_upload_pdf(uploaded_file) -> dict[str, Any]:
    response = requests.post(
        UPLOAD_API,
        files={"file": (uploaded_file.name, uploaded_file, "application/pdf")},
        timeout=300,
    )
    response.raise_for_status()
    return response.json()


def api_query(question: str) -> str:
    response = requests.post(QUERY_API, params={"question": question}, timeout=300)
    response.raise_for_status()
    payload = response.json()
    answer = payload.get("answer", "")
    if isinstance(answer, list):
        answer = "\n\n".join(answer)
    return answer


def api_chroma_summary(limit: int = 30) -> dict[str, Any]:
    response = requests.get(CHROMA_SUMMARY_API, params={"limit": limit}, timeout=120)
    response.raise_for_status()
    return response.json()


def api_clear_chroma() -> dict[str, Any]:
    response = requests.delete(CHROMA_CLEAR_API, timeout=60)
    response.raise_for_status()
    return response.json()
