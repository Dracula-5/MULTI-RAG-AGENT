from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.qa import router as qa_router
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qa_router)
