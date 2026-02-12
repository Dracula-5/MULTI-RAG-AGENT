from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from ..config import DATA_DIR


def _load_documents(folder: Path):
    docs = []
    if not folder.exists():
        return docs

    for file_path in folder.iterdir():
        if file_path.is_file():
            docs.extend(TextLoader(str(file_path), encoding="utf-8").load())
    return docs


def ingest_folder(folder: Path):
    docs = _load_documents(folder)
    if not docs:
        return False

    db = FAISS.from_documents(docs, OpenAIEmbeddings())
    db.save_local(str(folder))
    return True


def ingest_all_default_folders():
    targets = [
        DATA_DIR / "hr_docs",
        DATA_DIR / "engineering_docs",
        DATA_DIR / "sales_docs",
        DATA_DIR / "finance_docs",
        DATA_DIR / "legal_docs",
        DATA_DIR / "marketing_docs",
    ]
    ingested_any = False
    for target in targets:
        ingested_any = ingest_folder(target) or ingested_any
    return ingested_any
