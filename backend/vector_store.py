from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import os

# Shared vector DB directory
VECTOR_DB_PATH = "db/user_memory"

# Embeddings
import os
embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))


# Initialize Chroma DB
def get_memory_db():
    if not os.path.exists(VECTOR_DB_PATH):
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    return Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embedding)

# Store Q&A as memory
def store_memory(question: str, answer: str):
    vectordb = get_memory_db()
    text = f"Q: {question}\nA: {answer}"
    doc = Document(page_content=text, metadata={"source": "user_chat"})
    vectordb.add_documents([doc])
    vectordb.persist()

# Recall top similar memory
def recall_similar(query: str, top_k=2):
    vectordb = get_memory_db()
    results = vectordb.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]
