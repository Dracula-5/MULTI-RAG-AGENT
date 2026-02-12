import os
from langchain_classic.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from .tools import tools

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0,
)

executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True,
)

def ask(question):
    return executor.invoke({"input": question})["output"]
