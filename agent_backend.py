import sys
import types

# ---- Windows fix for missing 'pwd' module ----
if sys.platform == "win32":
    sys.modules["pwd"] = types.ModuleType("pwd")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RetrievalQA

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


# -------------------------------------------------
# GEMINI MODEL
# -------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3,
    convert_system_message_to_human=True
)

# -------------------------------------------------
# MEMORY
# -------------------------------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="input"
)

# -------------------------------------------------
# PROMPT (Learning + Notes)
# -------------------------------------------------
prompt = PromptTemplate(
    input_variables=["chat_history", "input"],
    template="""
You are an AI Learning Assistant.

RULES:
- Use very simple English
- Explain step by step
- Use real-life examples
- Use headings like Step 1, Step 2
- If mode is NOTES, write short exam-ready notes
- Do NOT generate quizzes

Conversation so far:
{chat_history}

User Input:
{input}

Answer:
"""
)

# -------------------------------------------------
# LEARNING CHAIN (ALWAYS AVAILABLE)
# -------------------------------------------------
learning_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

# -------------------------------------------------
# GLOBAL RAG CHAIN (OPTIONAL)
# -------------------------------------------------
rag_chain = None   # <-- NEW


def ai_tutor(topic, level="Beginner", mode="LEARN"):
    """
    Normal learning (NO PDF)
    """
    user_input = f"""
Topic: {topic}
Learning Level: {level}
Mode: {mode}
"""
    return learning_chain.run(input=user_input)


# -------------------------------------------------
# LOAD PDF (OPTIONAL)
# -------------------------------------------------
def load_pdf_rag(pdf_path):
    """
    Load PDF and enable RAG
    """
    global rag_chain

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False}
    )

    vectorstore = FAISS.from_documents(docs, embeddings)

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff"
    )

    return "PDF loaded successfully."


# -------------------------------------------------
# MAIN CHAT FUNCTION (SMART SWITCH)
# -------------------------------------------------
def chat(user_message):
    """
    If PDF is loaded → use RAG
    Else → normal learning
    """
    if rag_chain is not None:
        return rag_chain.run(user_message)
    else:
        return learning_chain.run(input=user_message)


# -------------------------------------------------
# REMOVE PDF (OPTIONAL)
# -------------------------------------------------
def clear_pdf():
    """
    Disable PDF-based learning
    """
    global rag_chain
    rag_chain = None
    return "PDF removed. Back to normal learning."
