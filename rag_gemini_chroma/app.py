import os

if __name__ != "__main__":
    # Preserve compatibility with `uvicorn app.main:app` by making this module
    # behave like a package when imported.
    __path__ = [os.path.join(os.path.dirname(__file__), "app")]
else:
    import streamlit as st

    from ui_utils import ensure_state, load_css, set_background

    HOME_BG = r"C:/BayGrape/rag_gemini_chroma/background_assets/image 1.jpg"

    def render_home() -> None:
        st.set_page_config(page_title="RAG Studio", page_icon="RAG", layout="wide")
        ensure_state()
        load_css()
        set_background(HOME_BG)

        st.markdown(
            """
            <section class="home-wrap">
                <h1>RAG Application</h1>
                <p>Select a module to continue</p>
            </section>
            """,
            unsafe_allow_html=True,
        )

        center_col = st.columns([1, 2, 1])[1]
        with center_col:
            if st.button("Embed Documents", key="card_embed", use_container_width=True):
                st.switch_page("pages/embed.py")
            if st.button("Chatbot", key="card_chat", use_container_width=True):
                st.switch_page("pages/chatbot.py")
            if st.button("View Chroma DB", key="card_db", use_container_width=True):
                st.switch_page("pages/chroma_db.py")

    render_home()
