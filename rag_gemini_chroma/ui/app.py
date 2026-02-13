import requests
import streamlit as st

UPLOAD_API = "http://127.0.0.1:8000/upload"
QUERY_API = "http://127.0.0.1:8000/query"
CHROMA_SUMMARY_API = "http://127.0.0.1:8000/chroma/summary"
CHROMA_CLEAR_API = "http://127.0.0.1:8000/chroma/clear"

st.set_page_config(page_title="RAG Studio", page_icon="RAG", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(900px 450px at 8% 0%, #d7f9ff 0%, transparent 60%),
            radial-gradient(900px 450px at 92% 8%, #d9fbd8 0%, transparent 55%),
            linear-gradient(130deg, #f3f8ff, #e8f7ec);
    }

    .hero {
        border: 1px solid #bfece5;
        border-radius: 14px;
        background: linear-gradient(140deg, #ffffffdd, #f2fffbdd);
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.8rem;
    }

    .hero h1 { margin: 0; color: #0b4b45; }
    .hero p { margin: 0.25rem 0 0; color: #1a3e43; }

    div.stButton > button {
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #1f3f52 !important;
    }

    div.stButton > button:hover { color: #111111 !important; }

    div[data-testid="stMetric"] {
        border: 1px solid #cdebe7;
        border-radius: 12px;
        background: #ffffffda;
        padding: 0.45rem;
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricValue"] {
        color: #111111 !important;
    }

    div[data-testid="stFileUploaderDropzone"] {
        background: #1f2433 !important;
        border: 1px solid #2e4e66 !important;
    }

    div[data-testid="stFileUploaderDropzone"] * {
        color: #f2f8ff !important;
    }

    div[data-testid="stChatMessage"] {
        background: #ffffffd9;
        border: 1px solid #d1ece8;
        border-radius: 12px;
    }

    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] div,
    div[data-testid="stChatMessage"] span {
        color: #122025 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chroma_loaded" not in st.session_state:
    st.session_state.chroma_loaded = None
if "show_attach" not in st.session_state:
    st.session_state.show_attach = False

with st.sidebar:
    st.title("RAG Menu")
    active_view = st.radio("Open", ["ChatBot", "ChromaDB"], label_visibility="collapsed")

st.markdown(
    """
    <div class="hero">
        <h1>RAG PDF Studio</h1>
        <p>Chat with your PDFs and explore Chroma vectors.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if active_view == "ChatBot":
    st.subheader("ChatBot")

    top_left, top_right = st.columns([1, 5])
    with top_left:
        if st.button("+ Attach PDF", use_container_width=True):
            st.session_state.show_attach = not st.session_state.show_attach
    with top_right:
        st.caption("Use + Attach PDF to upload a document before asking questions.")

    selected_pdf = None
    if st.session_state.show_attach:
        selected_pdf = st.file_uploader("Attach PDF", type=["pdf"], key="chat_pdf_uploader")
        if selected_pdf:
            st.success(f"Attached: {selected_pdf.name}")
            if st.button("Upload PDF", use_container_width=True):
                with st.spinner("Uploading and embedding PDF..."):
                    try:
                        upload_res = requests.post(
                            UPLOAD_API,
                            files={"file": (selected_pdf.name, selected_pdf, "application/pdf")},
                            timeout=300,
                        )
                        if upload_res.ok:
                            payload = upload_res.json()
                            st.success(
                                f"Embedded `{payload.get('source', selected_pdf.name)}` with "
                                f"{payload.get('chunks_ingested', 0)} chunks."
                            )
                            st.session_state.show_attach = False
                        else:
                            st.error(f"Upload failed: {upload_res.text}")
                    except Exception as e:
                        st.error(f"Upload error: {e}")

    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)

    prompt = st.chat_input("Ask about your uploaded PDF...")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("Generating answer..."):
            try:
                query_res = requests.post(QUERY_API, params={"question": prompt}, timeout=300)
                if query_res.ok:
                    answer = query_res.json().get("answer", "")
                    if isinstance(answer, list):
                        answer = "\n\n".join(answer)
                else:
                    answer = f"Query failed: {query_res.text}"
            except Exception as e:
                answer = f"Query error: {e}"

        with st.chat_message("assistant"):
            st.write(answer)
        st.session_state.chat_history.append((prompt, answer))

if active_view == "ChromaDB":
    st.subheader("ChromaDB")
    col_a, col_b = st.columns(2)
    with col_a:
        load_clicked = st.button("Load Chroma Data", use_container_width=True)
    with col_b:
        clear_clicked = st.button("Clear ChromaDB", use_container_width=True)

    if clear_clicked:
        with st.spinner("Clearing Chroma collection..."):
            try:
                clear_res = requests.delete(CHROMA_CLEAR_API, timeout=60)
                if clear_res.ok:
                    st.success("Chroma collection cleared.")
                    st.session_state.chroma_loaded = None
                else:
                    st.error(f"Clear failed: {clear_res.text}")
            except Exception as e:
                st.error(f"Clear error: {e}")

    if load_clicked or st.session_state.chroma_loaded is None:
        with st.spinner("Loading Chroma data..."):
            try:
                chroma_res = requests.get(CHROMA_SUMMARY_API, params={"limit": 25}, timeout=120)
                if chroma_res.ok:
                    st.session_state.chroma_loaded = chroma_res.json()
                else:
                    st.error(f"Load failed: {chroma_res.text}")
            except Exception as e:
                st.error(f"Load error: {e}")

    chroma_data = st.session_state.chroma_loaded
    if chroma_data:
        metric_a, metric_b, metric_c = st.columns(3)
        metric_a.metric("Vectors", chroma_data.get("vector_count", 0))
        metric_b.metric("Sources", chroma_data.get("source_count", 0))
        metric_c.metric("Avg chars/chunk", chroma_data.get("avg_chunk_chars", 0.0))

        st.caption(f"Collection: {chroma_data.get('collection_name', 'unknown')}")
        sources = chroma_data.get("sources", [])
        if sources:
            st.write("Sources:", ", ".join(sources))
        else:
            st.info("No sources in collection yet.")

        rows = chroma_data.get("preview_rows", [])
        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("No vector rows to preview.")
