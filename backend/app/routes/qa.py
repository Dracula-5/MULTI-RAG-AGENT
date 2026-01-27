from fastapi import APIRouter, UploadFile, File
from backend.app.agents.qa_agent import ask
import shutil
import os
import subprocess

router = APIRouter()

@router.post("/ask")
def ask_question(data: dict):
    question = data.get("question")
    if not question:
        return {"answer": "Please provide a question."}

    answer = ask(question)
    return {"answer": answer}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save to data/hr_docs/ for example
    path = f"data/hr_docs/{file.filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Run ingest script
    subprocess.run(["python", "../scripts/ingest_docs.py"])
    
    return {"message": "File uploaded and ingested"}
