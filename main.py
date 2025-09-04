from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-oss:20b", api_key="ollama", base_url="http://localhost:11434/v1")

tools = []
agent_executor = create_react_agent(llm, tools)

response = agent_executor.invoke({"messages": [("user", "explain artificial intelligence")]})

for message in response['messages']:
    print(message.content)