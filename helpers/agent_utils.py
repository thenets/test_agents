import time
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import create_react_agent
from .llm_config import configure_llm
from .calculator_tools import get_calculator_tools

def create_calculator_agent():
    """Create a ReAct agent with calculator tools"""
    llm = configure_llm()
    tools = get_calculator_tools()
    
    # Create the ReAct agent with calculator tools and system prompt
    agent = create_react_agent(
        llm, 
        tools,
        prompt="""You are a helpful calculator assistant. When asked to perform mathematical calculations, 
        you should use the provided calculator tools (add, subtract, multiply, divide) to compute the results accurately.
        Always use the tools for calculations rather than doing math in your head."""
    )
    
    return agent

def print_tool_execution_details(chunk):
    """Print detailed information about tool execution"""
    for node, data in chunk.items():
        if 'messages' in data:
            for message in data['messages']:
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    print(f"\n🔧 Tool Calls from {node}:")
                    for tool_call in message.tool_calls:
                        print(f"   Tool: {tool_call['name']}")
                        print(f"   Args: {tool_call['args']}")
                        print(f"   ID: {tool_call['id']}")
                
                elif isinstance(message, ToolMessage):
                    print(f"\n✅ Tool Result:")
                    print(f"   Tool: {message.name}")
                    print(f"   Result: {message.content}")
                
                elif isinstance(message, AIMessage) and not hasattr(message, 'tool_calls'):
                    print(f"\n🤖 AI Response from {node}:")
                    print(f"   {message.content}")

def run_calculation(agent, query):
    """Run a calculation query and show detailed execution"""
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print('='*60)
    
    start_time = time.time()
    
    # Stream the agent execution to see tool calls
    result = None
    for chunk in agent.stream({"messages": [HumanMessage(content=query)]}):
        print_tool_execution_details(chunk)
        result = chunk
    
    end_time = time.time()
    
    # Get the final answer
    if result and 'agent' in result and 'messages' in result['agent']:
        final_message = result['agent']['messages'][-1]
        if isinstance(final_message, AIMessage):
            print(f"\n🎯 FINAL ANSWER: {final_message.content}")
    
    print(f"\n⏱️  Execution time: {end_time - start_time:.2f} seconds")
    print(f"{'='*60}")
    
    return result