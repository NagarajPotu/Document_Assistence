import requests
import streamlit as st
import textwrap
import time
from extractor import extract_pdf_text, read_excel  # your own functions

# ----------------- Configuration -----------------
st.set_page_config(
    page_title="Nagaraj Document Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom Theme (Black + Blue + Glassmorphism) -----------------
st.markdown("""
<style>
:root {
    --main-bg: #000000; /* Main background black */
    --button-bg: #0284c7; /* Buttons / sidebar blue */
    --button-hover: #0369a1;
    --blur-amount: 18px;
    --border-color-light: rgba(255, 255, 255, 0.3);
    --border-color-dark: rgba(255, 255, 255, 0.15);
}

/* Main app background */
.stApp {
    background-color: var(--main-bg);
    color: #f9fafb;
}

/* Title */
.main-title {
    font-size: 2.4rem !important;
    color: #ffffff !important; /* White heading */
    text-align: center;
    font-weight: 800;
    margin-bottom: 0.5em;
    letter-spacing: -0.02em;
}

/* Chat Bubbles */
div[data-testid="stChatMessage"] {
    border-radius: 18px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(var(--blur-amount));
    -webkit-backdrop-filter: blur(var(--blur-amount));
    border: 1px solid var(--border-color-light);
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

/* User Message */
div[data-testid="stChatMessage-user"] {
    background: rgba(30, 30, 30, 0.7);
    color: #ffffff;
}

/* Assistant Message - force black text */
div[data-testid="stChatMessage-assistant"] {
    background: rgba(2, 132, 199, 0.9); /* Blue bubble */
    color: #000000 !important;
    font-weight: 500;
}
div[data-testid="stChatMessage-assistant"] * {
    color: #000000 !important; /* force black text in bubble */
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--button-bg) !important;
    color: #ffffff;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255,255,255,0.3);
}

/* Upload Box */
.upload-section {
    border: 2px dashed #ffffff;
    border-radius: 12px;
    padding: 16px;
    background: rgba(2, 132, 199, 0.7);
    backdrop-filter: blur(10px);
    text-align: center;
    color: #ffffff;
}

/* Buttons */
div.stButton>button {
    background-color: var(--button-bg);
    color: white;
    border-radius: 10px;
    padding: 0.6em 1em;
    font-weight: 600;
    transition: all 0.2s ease-in-out;
    border: none;
}
div.stButton>button:hover {
    background-color: var(--button-hover);
    transform: scale(1.06);
}

/* Chat Input */
.stChatInputContainer {
    backdrop-filter: blur(15px);
    background: rgba(30,30,30,0.8);
    border-top: 1px solid rgba(255,255,255,0.15);
}

/* Info Box */
.stInfo {
    background-color: rgba(2, 132, 199, 0.7) !important;
    border-left: 5px solid #ffffff !important;
    backdrop-filter: blur(8px);
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ----------------- Ollama Config -----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

# ----------------- Functions -----------------
def ask_ollama(prompt):
    data = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=data)
    return response.json()["response"]

def chunk_text(text, max_length=2000):
    return textwrap.wrap(text, max_length)

def ask_ollama_with_chunks(prompt, context):
    chunks = chunk_text(context, max_length=2000)
    replies = []
    for i, chunk in enumerate(chunks):
        full_prompt = f"Context (chunk {i+1}/{len(chunks)}):\n{chunk}\n\nQuestion:\n{prompt}"
        reply = ask_ollama(full_prompt)
        replies.append(reply)
    return " ".join(replies)

# ----------------- Title -----------------
st.markdown('<h1 class="main-title">📊 Nagaraj Document Assistant</h1>', unsafe_allow_html=True)
st.caption("💡 AI-powered assistant to analyze your PDFs and Excel financial data with Llama3")

# ----------------- Session State -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "doc_context" not in st.session_state:
    st.session_state.doc_context = ""

if "upload_status" not in st.session_state:
    st.session_state.upload_status = "No file uploaded"

# ----------------- Sidebar -----------------
with st.sidebar:
    st.header("📂 Upload a Document")
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload a PDF or Excel file", type=["pdf", "xlsx", "xls"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.button("🧹 Clear Chat", on_click=lambda: st.session_state.update(messages=[]))
    st.write("---")
    st.subheader("📊 Status")
    st.info(st.session_state.upload_status)

# ----------------- File Upload Handling -----------------
if uploaded:
    st.session_state.upload_status = "Uploading file..."
    status_bar = st.progress(0)

    for percent in range(0, 101, 25):
        time.sleep(0.1)
        status_bar.progress(percent)

    with st.spinner("🔍 Processing your document..."):
        if uploaded.name.endswith(".pdf"):
            st.session_state.doc_context = extract_pdf_text(uploaded)
        else:
            excel_data = read_excel(uploaded)
            st.session_state.doc_context = str(excel_data)

    st.session_state.upload_status = f"✅ Uploaded: {uploaded.name}"
    status_bar.empty()

# ----------------- Display Chat Messages -----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------- Chat Input -----------------
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            if st.session_state.doc_context:
                reply = ask_ollama_with_chunks(prompt, st.session_state.doc_context)
            else:
                reply = ask_ollama(prompt)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
