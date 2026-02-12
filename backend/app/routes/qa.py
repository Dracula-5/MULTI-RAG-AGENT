from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..agents.qa_agent import ask
from ..schemas import QueryRequest, QueryResponse
from ..services.ingest_service import ingest_folder
from ..config import DATA_DIR

router = APIRouter()


@router.post("/ask")
def ask_question(data: QueryRequest) -> QueryResponse:
    question = data.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Please provide a question.")

    try:
        answer = ask(question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process question: {exc}") from exc

    return QueryResponse(answer=answer)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    safe_name = Path(file.filename).name
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid filename.")

    hr_docs_dir = DATA_DIR / "hr_docs"
    hr_docs_dir.mkdir(parents=True, exist_ok=True)
    save_path = hr_docs_dir / safe_name

    contents = await file.read()
    save_path.write_bytes(contents)

    ingested = ingest_folder(hr_docs_dir)
    if not ingested:
        raise HTTPException(status_code=500, detail="File uploaded but ingestion failed.")

    return {"message": "File uploaded and ingested"}
