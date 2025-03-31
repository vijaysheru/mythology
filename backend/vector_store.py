from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_memory_db():
    return Chroma(embedding_function=embedding)  # no persistence

def store_memory(question: str, answer: str):
    vectordb = get_memory_db()
    doc = Document(page_content=f"Q: {question}\nA: {answer}")
    vectordb.add_documents([doc])

def recall_similar(query: str, top_k=2):
    vectordb = get_memory_db()
    results = vectordb.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]
