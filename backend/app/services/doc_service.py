from .vector_service import search
from ..config import DATA_DIR


def hr_docs(q): return search(q, str(DATA_DIR / "hr_docs"))


def eng_docs(q): return search(q, str(DATA_DIR / "engineering_docs"))


def sales_docs(q): return search(q, str(DATA_DIR / "sales_docs"))


def finance_docs(q): return search(q, str(DATA_DIR / "finance_docs"))


def legal_docs(q): return search(q, str(DATA_DIR / "legal_docs"))


def marketing_docs(q): return search(q, str(DATA_DIR / "marketing_docs"))
