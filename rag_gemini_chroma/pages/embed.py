import requests
import streamlit as st

from ui_utils import api_upload_pdf, ensure_state, load_css, set_background, show_loader, sidebar_nav

EMBED_BG = r"C:/BayGrape/rag_gemini_chroma/background_assets/image 2.jpg"


def render_embed() -> None:
    st.set_page_config(page_title="Embed Documents", page_icon="📄", layout="wide")
    ensure_state()
    load_css()
    set_background(EMBED_BG)
    sidebar_nav("Embed Documents")

    st.markdown('<h1 class="page-title">Embed Documents</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Upload a PDF, generate embeddings, and store chunks in ChromaDB.</p>',
        unsafe_allow_html=True,
    )

    wrap_col = st.columns([1, 1.7, 1])[1]
    with wrap_col:
        uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"], key="embed_pdf_uploader")

        if uploaded_pdf:
            st.markdown(f'<div class="chip-ok">Selected: {uploaded_pdf.name}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="chip-muted">No PDF selected.</div>', unsafe_allow_html=True)

        if st.button("Start Embedding", use_container_width=True):
            if not uploaded_pdf:
                st.error("Please select a PDF file first.")
            else:
                loader = show_loader("Embedding...")
                try:
                    payload = api_upload_pdf(uploaded_pdf)
                    st.success(
                        f"Embedded `{payload.get('source', uploaded_pdf.name)}` with "
                        f"{payload.get('chunks_ingested', 0)} chunks."
                    )
                except requests.RequestException as exc:
                    st.error(f"Embedding failed: {exc}")
                finally:
                    loader.empty()


render_embed()
