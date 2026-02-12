from langchain_classic.tools import Tool
from ..services.doc_service import hr_docs, eng_docs
from ..services.email_service import search_emails
from ..services.sql_service import run_sql

tools = [
    Tool(name="HR_Docs", func=hr_docs, description="Search HR policies"),
    Tool(name="Engineering_Docs", func=eng_docs, description="Search engineering docs"),
    Tool(name="Emails", func=search_emails, description="Search emails"),
    Tool(name="SQL_DB", func=run_sql, description="Query company database"),
]
