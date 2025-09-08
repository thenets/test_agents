# from typing import Literal  # Removed as not needed with simplified type hints
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from tools import get_tools, get_tools_by_name

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

# Initialize LLM and tools
llm = configure_llm()
tools = get_tools()
tools_by_name = get_tools_by_name()
llm_with_tools = llm.bind_tools(tools)

# Nodes
def llm_call(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    
    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
                ]
                + state["messages"]
            )
        ]
    }

def tool_node(state: MessagesState):
    """Performs the tool call"""
    
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"], name=tool_call["name"]))
    return {"messages": result}

# Conditional edge function to route to the tool node or end based upon whether the LLM made a tool call
def should_continue(state: MessagesState):
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    
    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "environment"
    # Otherwise, we stop (reply to the user)
    return END

def create_agent():
    """Build and compile the agent"""
    
    # Build workflow
    agent_builder = StateGraph(MessagesState)
    
    # Add nodes
    agent_builder.add_node("llm_call", llm_call)
    agent_builder.add_node("environment", tool_node)
    
    # Add edges to connect nodes
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        {
            # Name returned by should_continue : Name of next node to visit
            "environment": "environment",
            END: END,
        },
    )
    agent_builder.add_edge("environment", "llm_call")
    
    # Compile the agent
    return agent_builder.compile()

def print_step_details(step_num, chunk):
    """Print detailed information about each step in the agent loop"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}")
    print('='*60)
    
    for node_name, data in chunk.items():
        print(f"\n🔵 Node: {node_name}")
        
        if 'messages' in data:
            for message in data['messages']:
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    print(f"🤖 AI Message with Tool Calls:")
                    for tool_call in message.tool_calls:
                        print(f"   Tool: {tool_call['name']}")
                        print(f"   Args: {tool_call['args']}")
                        print(f"   ID: {tool_call['id']}")
                
                elif isinstance(message, ToolMessage):
                    print(f"🛠️  Tool Result:")
                    print(f"   Tool: {message.name}")
                    print(f"   Result: {message.content}")
                
                elif hasattr(message, 'content') and (not hasattr(message, 'tool_calls') or not message.tool_calls):
                    print(f"💬 AI Response:")
                    print(f"   {message.content}")

def run_agent_example(query: str):
    """Run the agent with a specific query and show the loop in action"""
    print(f"\n{'🚀 AGENT EXECUTION':<60}")
    print(f"Query: {query}")
    print('='*80)
    
    agent = create_agent()
    
    # Run the agent and show each step
    step_num = 1
    for chunk in agent.stream({"messages": [HumanMessage(content=query)]}):
        print_step_details(step_num, chunk)
        step_num += 1
    
    print(f"\n{'✅ EXECUTION COMPLETE':<60}")
    print('='*80)

def main():
    """Main function demonstrating the simple agent loop"""
    print("LangGraph Simple Agent Loop Example")
    print("=" * 50)
    print("This example demonstrates the core agent pattern:")
    print("LLM → Tool Call → Environment → Loop back → Exit")
    print("\nKey concepts:")
    print("• Agent loops until no more tool calls are needed")
    print("• Each iteration: reason → act → observe")
    print("• Natural exit when task is complete")
    
    # Test cases demonstrating multi-step reasoning
    test_cases = [
        "Add 3 and 4",
        "Add 3 and 4. Then, take the output and multiply by 4.",
        "Calculate (15 + 25) divided by 2, then multiply by 3",
        "Start with 10, add 5, multiply by 2, then subtract 3"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n\n{'='*80}")
        print(f"TEST CASE {i}/{len(test_cases)}")
        print('='*80)
        
        try:
            run_agent_example(query)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n\n{'🎉 ALL TESTS COMPLETED!':<60}")
    print("=" * 80)
    print("\nWhat we learned:")
    print("• How agents loop between reasoning and action")
    print("• When and why loops terminate (no more tool calls)")
    print("• How state accumulates through iterations")
    print("• Multi-step problem solving in action")

if __name__ == "__main__":
    main()