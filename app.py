import requests
import streamlit as st
import textwrap
import time
from extractor import extract_pdf_text, read_excel  # your own functions

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"   # or "gemma2:2b" if you pulled it

# ----------------- Function to talk to Ollama -----------------
def ask_ollama(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=data)
    return response.json()["response"]

# ----------------- Helper: Chunk large text -----------------
def chunk_text(text, max_length=2000):
    """Splits long text into chunks of max_length characters."""
    return textwrap.wrap(text, max_length)

def ask_ollama_with_chunks(prompt, context):
    """Ask Ollama with document split into chunks."""
    chunks = chunk_text(context, max_length=2000)
    replies = []
    for i, chunk in enumerate(chunks):
        full_prompt = f"Context (chunk {i+1}/{len(chunks)}):\n{chunk}\n\nQuestion:\n{prompt}"
        reply = ask_ollama(full_prompt)
        replies.append(reply)
    return " ".join(replies)

# ----------------- Streamlit UI -----------------
st.title("📊 Nagaraj Financial Document Assistant")

# ----------------- Initialize session state -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "doc_context" not in st.session_state:
    st.session_state.doc_context = ""

if "upload_status" not in st.session_state:
    st.session_state.upload_status = "No file uploaded"

# ----------------- Clear chat function -----------------
def clear_chat():
    st.session_state.messages = []

# ----------------- File uploader + Clear Chat side by side -----------------
col1, col2 = st.columns([4, 1])

with col1:
    uploaded = st.file_uploader("Upload a PDF or Excel", type=["pdf", "xlsx", "xls"])

with col2:
    st.button("Clear Chat", on_click=clear_chat)

# ----------------- Handle file upload -----------------
if uploaded:
    st.session_state.upload_status = "Uploading file..."
    status_bar = st.progress(0)

    # Simulate progress bar
    for percent in range(0, 101, 25):
        time.sleep(0.1)
        status_bar.progress(percent)

    with st.spinner("Processing document..."):
        if uploaded.name.endswith(".pdf"):
            st.session_state.doc_context = extract_pdf_text(uploaded)
        else:
            excel_data = read_excel(uploaded)
            st.session_state.doc_context = str(excel_data)

    st.session_state.upload_status = f"Uploaded: {uploaded.name}"
    status_bar.empty()  # remove progress bar after done

# ----------------- Show upload status -----------------
st.info(st.session_state.upload_status)

# ----------------- Show past messages -----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------- Chat input -----------------
if prompt := st.chat_input("Ask a financial question..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Answer with document context
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.doc_context:
                reply = ask_ollama_with_chunks(prompt, st.session_state.doc_context)
            else:
                reply = ask_ollama(prompt)  # fallback if no file uploaded
            st.markdown(reply)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
