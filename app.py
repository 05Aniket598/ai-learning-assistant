import streamlit as st
import tempfile

from agent_backend import (
    load_pdf_rag,
    chat,
    clear_pdf
)

st.set_page_config(
    page_title="AI Learning Assistant",
    layout="wide"
)

st.title("📘 AI Learning Assistant")

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# SIDEBAR: LEARNING SETTINGS
# -------------------------------------------------
st.sidebar.header("Learning Settings")

mode = st.sidebar.selectbox(
    "Mode",
    ["LEARN", "NOTES"]
)

level = st.sidebar.selectbox(
    "Learning Level",
    ["Beginner", "Intermediate", "Advanced"]
)

st.sidebar.divider()

# -------------------------------------------------
# SIDEBAR: PDF UPLOAD
# -------------------------------------------------
st.sidebar.header("Optional PDF Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF (optional)",
    type=["pdf"]
)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    load_pdf_rag(pdf_path)
    st.sidebar.success("PDF loaded. Answers will use PDF context.")

if st.sidebar.button("Remove PDF"):
    clear_pdf()
    st.sidebar.info("PDF removed. Back to normal learning.")

# -------------------------------------------------
# CHAT HISTORY
# -------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------------------------
# CHAT INPUT
# -------------------------------------------------
user_input = st.chat_input("Ask a question...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    backend_input = f"""
Topic: {user_input}
Learning Level: {level}
Mode: {mode}
"""

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat(backend_input)
            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
