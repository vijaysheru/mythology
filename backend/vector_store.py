from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# In-memory vector DB
db = DocArrayInMemorySearch.from_texts([], embedding)

def store_memory(question: str, answer: str):
    global db
    text = f"Q: {question}\nA: {answer}"
    doc = Document(page_content=text)
    db.add_documents([doc])

def recall_similar(query: str, top_k=2):
    global db
    results = db.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results] if results else ["🧠 Krishna has no memory yet."]
