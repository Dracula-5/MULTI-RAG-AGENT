from .vector_service import search

def hr_docs(q): return search(q, "data/hr_docs")
def eng_docs(q): return search(q, "data/engineering_docs")
def sales_docs(q): return search(q, "data/sales_docs")
def finance_docs(q): return search(q, "data/finance_docs")
def legal_docs(q): return search(q, "data/legal_docs")
def marketing_docs(q): return search(q, "data/marketing_docs")
