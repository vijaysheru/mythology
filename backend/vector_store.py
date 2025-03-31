import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

# Secure API key for Together/OpenAI-compatible endpoints
embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Persistent path (local) — will fallback to memory if not writable
VECTOR_DB_PATH = "db/user_memory"

# Check if running on Streamlit Cloud (read-only FS)
IS_CLOUD = os.getenv("STREAMLIT_CLOUD") == "1"

# Initialize Chroma DB
def get_memory_db():
    try:
        if IS_CLOUD:
            # ✅ In-memory DB for Streamlit Cloud
            return Chroma(embedding_function=embedding)
        else:
            os.makedirs(VECTOR_DB_PATH, exist_ok=True)
            return Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embedding)
    except Exception as e:
        # Fallback if filesystem is not writable
        print("⚠️ Falling back to in-memory ChromaDB due to:", e)
        return Chroma(embedding_function=embedding)

# Store memory
def store_memory(question: str, answer: str):
    vectordb = get_memory_db()
    text = f"Q: {question}\nA: {answer}"
    doc = Document(page_content=text, metadata={"source": "user_chat"})
    vectordb.add_documents([doc])
    if not IS_CLOUD:
        vectordb.persist()

# Recall memory
def recall_similar(query: str, top_k=2):
    vectordb = get_memory_db()
    results = vectordb.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]
