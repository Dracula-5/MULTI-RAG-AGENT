from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

def ingest(folder, out):
    docs=[]
    for f in os.listdir(folder):
        docs+=TextLoader(folder+"/"+f).load()
    FAISS.from_documents(docs, OpenAIEmbeddings()).save_local(out)

ingest("data/hr_docs","data/hr_docs")
ingest("data/engineering_docs","data/engineering_docs")
ingest("data/sales_docs","data/sales_docs")
ingest("data/finance_docs","data/finance_docs")
ingest("data/legal_docs","data/legal_docs")
ingest("data/marketing_docs","data/marketing_docs")
