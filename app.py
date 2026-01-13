import streamlit as st
import tempfile

from agent_backend import (
    ai_tutor,
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
# SIDEBAR: OPTIONAL PDF UPLOAD
# -------------------------------------------------
st.sidebar.header("Optional: Upload Learning PDF")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF file (optional)",
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
# MAIN CHAT AREA
# -------------------------------------------------
st.subheader("Ask a Question")

question = st.text_input("Enter your question")

mode = st.selectbox(
    "Select Mode",
    ["LEARN", "NOTES"]
)

level = st.selectbox(
    "Learning Level",
    ["Beginner", "Intermediate", "Advanced"]
)

if st.button("Get Answer"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            user_message = f"""
            Topic: {question}
            Learning Level: {level}
            Mode: {mode}
            """
            answer = chat(user_message)

        st.markdown("### Answer")
        st.write(answer)
