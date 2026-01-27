import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
if not OPENAI_API_KEY or not DATABASE_URL or not SECRET_KEY:
    raise ValueError("Missing one or more required environment variables.")
