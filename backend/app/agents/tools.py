from langchain.tools import Tool
from ..services.doc_service import hr_docs, eng_docs
from ..services.email_service import search_emails
from ..services.sql_service import run_sql

tools = [
    Tool("HR_Docs", hr_docs, "Search HR policies"),
    Tool("Engineering_Docs", eng_docs, "Search engineering docs"),
    Tool("Emails", search_emails, "Search emails"),
    Tool("SQL_DB", run_sql, "Query company database")
]
