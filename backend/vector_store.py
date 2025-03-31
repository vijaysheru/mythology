import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

# Initialize embedding model
embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Global FAISS store in memory
# Initialize with an empty FAISS store
faiss_db = FAISS.from_documents([], embedding)

# 🧠 Store memory
def store_memory(question: str, answer: str):
    global faiss_db
    text = f"Q: {question}\nA: {answer}"
    doc = Document(page_content=text)
    faiss_db.add_documents([doc])

# 🔍 Recall similar past Q&A
def recall_similar(query: str, top_k=2):
    global faiss_db
    results = faiss_db.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]
