from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()


def load_db(path):
    vector_path = Path(path)
    if not vector_path.exists():
        return None
    return FAISS.load_local(str(vector_path), embeddings, allow_dangerous_deserialization=True)


def search(query, path):
    db = load_db(path)
    if db is None:
        return "No indexed documents found for this data source yet."
    docs = db.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])


def add_documents(docs, path):
    db = load_db(path)
    if db is None:
        return create_vector_store(docs, path)
    db.add_documents(docs)
    db.save_local(path)
    return True


def create_vector_store(docs, path):
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(path)
    return True

