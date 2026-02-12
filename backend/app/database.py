from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

normalized_database_url = DATABASE_URL
if normalized_database_url.startswith("postgres://"):
    normalized_database_url = normalized_database_url.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if normalized_database_url.startswith("sqlite") else {}

engine = create_engine(normalized_database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

