from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.qa import router as qa_router
from .routes.auth import router as auth_router
from .database import engine
from . import models
from .config import CORS_ORIGINS

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(qa_router)
app.include_router(auth_router)
