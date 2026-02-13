import requests
import streamlit as st

from ui_utils import (
    api_chroma_summary,
    api_clear_chroma,
    ensure_state,
    load_css,
    set_background,
    show_loader,
    sidebar_nav,
)

CHROMA_BG = r"C:/BayGrape/rag_gemini_chroma/background_assets/image4.avif"


def render_chroma() -> None:
    st.set_page_config(page_title="Chroma DB", page_icon="🗂️", layout="wide")
    ensure_state()
    load_css()
    set_background(CHROMA_BG)
    sidebar_nav("View Chroma DB")

    st.markdown('<h1 class="page-title">Chroma DB</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Inspect vectors, source files, and chunk previews stored in Chroma.</p>',
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns(2)
    with top_left:
        load_clicked = st.button("Load Database Summary", use_container_width=True)
    with top_right:
        clear_clicked = st.button("Clear Collection", use_container_width=True)

    if clear_clicked:
        loader = show_loader("Clearing...")
        try:
            api_clear_chroma()
            st.session_state.chroma_loaded = None
            st.success("Collection cleared.")
        except requests.RequestException as exc:
            st.error(f"Clear failed: {exc}")
        finally:
            loader.empty()

    if load_clicked or st.session_state.chroma_loaded is None:
        loader = show_loader("Loading...")
        try:
            st.session_state.chroma_loaded = api_chroma_summary(limit=40)
        except requests.RequestException as exc:
            st.error(f"Load failed: {exc}")
        finally:
            loader.empty()

    data = st.session_state.chroma_loaded
    if data:
        m1, m2, m3 = st.columns(3)
        m1.metric("Vectors", data.get("vector_count", 0))
        m2.metric("Sources", data.get("source_count", 0))
        m3.metric("Avg chars/chunk", data.get("avg_chunk_chars", 0.0))

        st.markdown(
            f'<div class="chip-muted">Collection: {data.get("collection_name", "unknown")}</div>',
            unsafe_allow_html=True,
        )

        sources = data.get("sources", [])
        if sources:
            st.markdown('<h3 class="section-title">Sources</h3>', unsafe_allow_html=True)
            st.write(", ".join(sources))
        else:
            st.info("No sources found.")

        st.markdown('<h3 class="section-title">Chunk Preview</h3>', unsafe_allow_html=True)
        preview_rows = data.get("preview_rows", [])
        if preview_rows:
            st.dataframe(preview_rows, use_container_width=True, hide_index=True)
        else:
            st.info("No chunk rows available.")


render_chroma()
