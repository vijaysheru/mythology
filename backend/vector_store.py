import os
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

# Use HuggingFace embeddings for full free usage
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Global in-memory FAISS DB
faiss_db = None

def store_memory(question: str, answer: str):
    global faiss_db
    doc = Document(page_content=f"Q: {question}\nA: {answer}")

    if faiss_db is None:
        faiss_db = FAISS.from_documents([doc], embedding)
    else:
        faiss_db.add_documents([doc])

def recall_similar(query: str, top_k=2):
    if faiss_db is None:
        return ["🧠 Krishna has no memory yet."]
    results = faiss_db.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]
