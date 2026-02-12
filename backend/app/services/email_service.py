from pathlib import Path
from ..config import DATA_DIR

EMAILS_DIR = DATA_DIR / "emails"


def _ensure_emails_dir():
    EMAILS_DIR.mkdir(parents=True, exist_ok=True)


def _safe_email_path(filename: str) -> Path:
    safe_name = Path(filename).name
    if not safe_name:
        raise ValueError("Invalid filename.")
    return EMAILS_DIR / safe_name


def search_emails(query):
    _ensure_emails_dir()
    hits = []
    for file_path in EMAILS_DIR.iterdir():
        if not file_path.is_file():
            continue
        content = file_path.read_text(encoding="utf-8")
        if query.lower() in content.lower():
            hits.append(file_path.name)
    return ", ".join(hits)


def list_emails():
    _ensure_emails_dir()
    return [file_path.name for file_path in EMAILS_DIR.iterdir() if file_path.is_file()]


def save_email(filename, content):
    _ensure_emails_dir()
    _safe_email_path(filename).write_text(content, encoding="utf-8")
    return True


def delete_email(filename):
    _ensure_emails_dir()
    _safe_email_path(filename).unlink(missing_ok=True)
    return True


def read_email(filename):
    _ensure_emails_dir()
    return _safe_email_path(filename).read_text(encoding="utf-8")


def update_email(filename, content):
    _ensure_emails_dir()
    _safe_email_path(filename).write_text(content, encoding="utf-8")
    return True


