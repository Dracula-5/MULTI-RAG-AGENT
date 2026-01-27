from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_openai import OpenAI
from .tools import tools

llm = OpenAI(temperature=0)

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def ask(question):
    return executor.invoke({"input": question})["output"]
