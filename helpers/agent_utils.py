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
                        print(f"   🛠️  {tool_call['name']}({tool_call['args']})")
                
                elif hasattr(message, 'invalid_tool_calls') and message.invalid_tool_calls:
                    print(f"\n❌ Invalid Tool Calls from {node}:")
                    for invalid_call in message.invalid_tool_calls:
                        print(f"   🚫 {invalid_call['name']}: {invalid_call.get('error', 'Invalid format')}")
                
                elif isinstance(message, ToolMessage):
                    print(f"\n✅ Tool Result:")
                    print(f"   🎯 {message.name} → {message.content}")
                
                elif isinstance(message, AIMessage) and message.content and not hasattr(message, 'tool_calls'):
                    print(f"\n🤖 AI Response from {node}:")
                    print(f"   💭 {message.content}")

def run_calculation(agent, query):
    """Run a calculation query and show detailed execution"""
    print(f"\n{'='*60}")
    print(f"🧮 QUERY: {query}")
    print('='*60)
    
    start_time = time.time()
    
    # Stream the agent execution to see tool calls
    result = None
    successful_calculation = False
    final_answer = None
    
    for chunk in agent.stream({"messages": [HumanMessage(content=query)]}):
        print_tool_execution_details(chunk)
        result = chunk
        
        # Check for successful tool execution
        if 'agent' in chunk and 'messages' in chunk['agent']:
            for message in chunk['agent']['messages']:
                if isinstance(message, ToolMessage):
                    successful_calculation = True
                    final_answer = message.content
                elif isinstance(message, AIMessage) and message.content:
                    final_answer = message.content
    
    end_time = time.time()
    
    # Display final result
    if successful_calculation and final_answer:
        print(f"\n🎯 FINAL ANSWER: {final_answer}")
        print(f"✅ Calculation completed successfully!")
    elif final_answer:
        print(f"\n🤖 FINAL RESPONSE: {final_answer}")
    else:
        print(f"\n❌ No valid result obtained")
    
    print(f"\n⏱️  Execution time: {end_time - start_time:.2f} seconds")
    print(f"{'='*60}")
    
    return result