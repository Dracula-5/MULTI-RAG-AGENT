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


def _build_detailed_prompt(question: str) -> str:
    return (
        "You are an enterprise knowledge assistant. "
        "Provide a complete, practical answer using clear sections. "
        "Always include: 1) direct answer, 2) supporting details, 3) concrete next steps. "
        "If uncertain, state assumptions clearly. "
        "Keep it concise but not one-line; target 5-10 sentences minimum when enough context exists.\n\n"
        f"User question: {question}"
    )


def ask(question):
    detailed_query = _build_detailed_prompt(question)
    return executor.invoke({"input": detailed_query})["output"]
