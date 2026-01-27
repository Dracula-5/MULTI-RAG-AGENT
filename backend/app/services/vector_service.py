from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

def load_db(path):
    return FAISS.load_local(path, embeddings)

def search(query, path):
    db = load_db(path)
    docs = db.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])
def add_documents(docs, path):
    db = load_db(path)
    db.add_documents(docs)
    db.save_local(path)
    return True
def create_vector_store(docs, path):
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(path)
    return True

