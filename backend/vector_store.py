import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

# ✅ Use OpenAI for embeddings
embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# In-memory FAISS vector DB
faiss_db = None

def store_memory(question: str, answer: str):
    global faiss_db
    text = f"Q: {question}\nA: {answer}"
    doc = Document(page_content=text)

    if faiss_db is None:
        faiss_db = FAISS.from_documents([doc], embedding)
    else:
        faiss_db.add_documents([doc])

def recall_similar(query: str, top_k=2):
    global faiss_db
    if faiss_db is None:
        return ["🧠 Krishna has no memory yet."]
    results = faiss_db.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]
