import requests
import streamlit as st

from ui_utils import (
    api_query,
    api_upload_pdf,
    ensure_state,
    load_css,
    set_background,
    show_loader,
    sidebar_nav,
)

CHATBOT_BG = r"C:/BayGrape/rag_gemini_chroma/background_assets/image 3.jpg"


def render_chatbot() -> None:
    st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")
    ensure_state()
    load_css()
    set_background(CHATBOT_BG)
    sidebar_nav("Chatbot")

    st.markdown('<h1 class="page-title">Chatbot</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Attach a PDF and chat with context-aware responses from your indexed data.</p>',
        unsafe_allow_html=True,
    )

    with st.expander("➕ Attach PDF", expanded=False):
        attached = st.file_uploader("Attach PDF", type=["pdf"], key="chat_attach_pdf")
        if attached and st.button("Upload Attached File", use_container_width=True):
            loader = show_loader("Uploading...")
            try:
                payload = api_upload_pdf(attached)
                st.success(
                    f"Embedded `{payload.get('source', attached.name)}` with "
                    f"{payload.get('chunks_ingested', 0)} chunks."
                )
            except requests.RequestException as exc:
                st.error(f"Upload failed: {exc}")
            finally:
                loader.empty()

    for user_text, bot_text in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(user_text)
        with st.chat_message("assistant"):
            st.markdown(bot_text)

    prompt = st.chat_input("Ask about your uploaded PDFs...")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        loader = show_loader("Thinking...")
        try:
            answer = api_query(prompt)
        except requests.RequestException as exc:
            answer = f"Query failed: {exc}"
        finally:
            loader.empty()

        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.chat_history.append((prompt, answer))


render_chatbot()
