# AI Learning Assistant

AI Learning Assistant is a beginner-friendly AI application that helps users learn concepts step by step.  
It uses the **Gemini language model** and **LangChain** to explain topics, generate notes, remember conversation context, and optionally learn from uploaded PDF documents.

The system is designed so that **PDF upload is optional**. Users can learn normally without uploading any file, and if a PDF is uploaded, the assistant automatically switches to document-based learning.

---

## Features

- Step-by-step explanation of concepts in simple English  
- Notes generation mode for exam preparation  
- Conversation memory for follow-up questions  
- Optional PDF-based learning using Retrieval-Augmented Generation (RAG)  
- Works with or without PDF upload  
- Ability to remove PDF and return to normal learning  
- Simple Streamlit-based user interface  

---

## Tech Stack

- **Programming Language:** Python  
- **LLM:** Google Gemini (gemini-2.5-flash-lite)  
- **Framework:** LangChain  
- **Frontend:** Streamlit  
- **Vector Store:** FAISS  
- **Embeddings:** Sentence-Transformers (local embeddings, no API quota)  

---

## Project Structure

AI Agent/
│
├── agent_backend.py # Backend logic (LLM, memory, optional RAG)
├── app.py # Streamlit frontend
├── requirements.txt # Project dependencies
├── README.md # Project documentation
└── .gitignore # Ignored files and folders


---

## How the System Works

- When no PDF is uploaded, the assistant behaves like a normal AI tutor using Gemini.
- When a PDF is uploaded, the backend dynamically enables RAG and answers using the PDF content.
- The user can remove the PDF at any time and continue normal learning.
- The frontend does not control this logic; the backend decides automatically.

This design keeps the system flexible and user-controlled.

---

## Installation and Setup

### 1. Create a virtual environment
python -m venv agent

### 2. Activate the environment (Windows)
agent\Scripts\Activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the application
streamlit run app.py


How to Use the Application

Open the Streamlit app in your browser

Enter a question to learn a concept

Choose LEARN mode for explanations or NOTES mode for short notes

Upload a PDF (optional) to enable document-based learning

Remove the PDF anytime to return to normal learning

Limitations

PDF embeddings are generated locally to avoid API quota limits

Performance depends on CPU when processing large PDF files

Academic Note

This project is developed for educational purposes to demonstrate:

Large Language Model (LLM) integration

Prompt engineering

Conversation memory

Retrieval-Augmented Generation (RAG)

Clean backend–frontend separation


Author

Aniket Yadav