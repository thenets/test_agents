from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

llm = ChatOpenAI(model="gpt-oss:20b", api_key="ollama", base_url="http://localhost:11434/v1")

search = DuckDuckGoSearchRun()

tools = [search]
agent_executor = create_react_agent(llm, tools)

query = "What are the latest developments in open source AI models in 2025?"
print(f"Query: {query}\n")

response = agent_executor.invoke({"messages": [("user", query)]})

for message in response['messages']:
    if hasattr(message, 'content') and message.content:
        print(f"{message.type}: {message.content}")
        print("-" * 50)