from pathlib import Path
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
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
        error_text = str(exc).lower()
        if "api key" in error_text:
            return QueryResponse(
                answer=(
                    "The assistant is not configured with a valid OpenAI API key. "
                    "Set OPENAI_API_KEY in backend environment variables and redeploy."
                )
            )
        if "insufficient_quota" in error_text or "error code: 429" in error_text:
            return QueryResponse(
                answer=(
                    "I cannot generate a live AI answer right now because the OpenAI API quota is exhausted. "
                    "Please top up billing or increase project limits, then retry. "
                    "If this persists, verify the API key belongs to the project with available credits."
                )
            )
        raise HTTPException(status_code=500, detail="Failed to process question due to a backend error.") from exc

    return QueryResponse(answer=answer)


def _ingest_hr_docs_background(hr_docs_dir: Path):
    ingest_folder(hr_docs_dir)


@router.post("/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    safe_name = Path(file.filename).name
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid filename.")

    hr_docs_dir = DATA_DIR / "hr_docs"
    hr_docs_dir.mkdir(parents=True, exist_ok=True)
    save_path = hr_docs_dir / safe_name

    with save_path.open("wb") as out_file:
        shutil.copyfileobj(file.file, out_file)

    background_tasks.add_task(_ingest_hr_docs_background, hr_docs_dir)

    return {"message": "File uploaded. Index refresh started in background."}
