import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import create_react_agent
from tools import get_calculator_tools

load_dotenv()

def configure_llm():
    """Configure the LLM with OpenRouter or local Ollama settings"""
    # Check if OpenRouter configuration is available
    """if os.getenv("OPENROUTER_API_KEY"):
        return ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL"),
            model=os.getenv("MODEL_NAME", "deepseek/deepseek-chat"),
            temperature=0.1  # Lower temperature for more consistent math
        )
    else:"""
        # Fallback to local Ollama
    return ChatOpenAI(
        model="mistral",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
        temperature=0.1
    )

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

def main():
    """Main function to run the calculator agent example"""
    print("LangGraph Calculator Tool Integration Example")
    print("=" * 50)
    
    # Check configuration
    if not os.getenv("OPENROUTER_API_KEY") and not os.path.exists("http://localhost:11434"):
        print("Warning: No OpenRouter API key found and Ollama may not be running.")
        print("Please set up your environment variables or start Ollama.")
    
    # Create the calculator agent
    agent = create_calculator_agent()
    
    # Test cases that force tool usage
    test_queries = [
        "Calculate 145 + 237",
        "What is 23 * 67?",
        "Compute 1024 divided by 8",
        "Find the result of 500 - 123",
        "What is 15.5 + 24.3?",
        "Calculate 999 / 3",
        "What's 2.5 * 4.8?",
        "Subtract 89 from 234"
    ]
    
    print(f"\nTesting {len(test_queries)} calculator queries...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n\n📊 Test {i}/{len(test_queries)}")
        try:
            run_calculation(agent, query)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Complex calculation test
    print(f"\n\n🧮 Complex Calculation Test")
    complex_query = "I need to calculate (15 + 25) * 3. Can you help me with this step by step?"
    try:
        run_calculation(agent, complex_query)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n\n🎉 Calculator agent testing completed!")
    print("\nThis example demonstrates:")
    print("• LangGraph ReAct agent with tool integration")
    print("• Custom calculator tools using @tool decorator")
    print("• Automatic tool selection and execution")
    print("• Detailed execution flow visualization")

if __name__ == "__main__":
    main()