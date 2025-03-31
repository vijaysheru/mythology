import os
from langchain_community.vectorstores import Chroma  # ✅ NEW
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

# Use Chroma with HuggingFace (no OpenAI required)
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

VECTOR_DB_PATH = "db"

# Initialize Chroma vector store
def get_memory_db():
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    return Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embedding)

# Store memory
def store_memory(question: str, answer: str):
    vectordb = get_memory_db()
    text = f"Q: {question}\nA: {answer}"
    doc = Document(page_content=text)
    vectordb.add_documents([doc])
    vectordb.persist()

# Recall memory
def recall_similar(query: str, top_k=2):
    vectordb = get_memory_db()
    results = vectordb.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]
