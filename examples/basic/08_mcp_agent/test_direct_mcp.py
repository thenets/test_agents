#!/usr/bin/env python3
"""
Test MCP tools directly without the ReAct agent to isolate functionality
"""

from simulated_mcp_wrapper import simulated_mcp_client

def test_direct_mcp_calls():
    """Test MCP tools directly"""
    print("🔧 Direct MCP Tools Test")
    print("=" * 40)
    
    # Get tools
    tools = simulated_mcp_client.get_langchain_tools()
    print(f"Available tools: {len(tools)}")
    
    # Test calculator directly
    print("\n🧮 Testing Calculator Add:")
    calc_add = tools[0]
    result = calc_add.invoke({"input_text": "15, 27"})
    print(f"15 + 27 = {result}")
    
    # Test calculator multiply
    print("\n🔢 Testing Calculator Multiply:")
    calc_mult = tools[1]
    result = calc_mult.invoke({"input_text": "8, 12"})
    print(f"8 × 12 = {result}")
    
    # Test web search
    print("\n🌐 Testing Web Search:")
    web_search = tools[2]
    result = web_search.invoke({"query": "Python programming"})
    print(f"Search result: {result[:150]}...")
    
    # Test file operations
    print("\n📁 Testing File List:")
    file_list = tools[4]
    result = file_list.invoke({"input_text": ""})
    print(f"Files: {result[:150]}...")

def test_simple_agent():
    """Test a very simple agent without ReAct complexity"""
    print("\n🤖 Testing Simple Agent")
    print("=" * 40)
    
    from langchain_openai import ChatOpenAI
    from langchain.agents import initialize_agent, AgentType
    
    # Create LLM
    llm = ChatOpenAI(
        model="gpt-oss:20b",
        api_key="ollama", 
        base_url="http://localhost:11434/v1"
    )
    
    # Get MCP tools
    tools = simulated_mcp_client.get_langchain_tools()
    
    # Create simple agent
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=2
    )
    
    # Simple query
    query = "Use the calculator to add 5 and 8"
    print(f"Query: {query}")
    
    try:
        result = agent.run(query)
        print(f"Result: {result}")
        return True
    except Exception as e:
        print(f"Agent error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Direct MCP Testing (No Agent)")
    print("=" * 50)
    
    # Test tools directly first
    test_direct_mcp_calls()
    
    # Then test simple agent
    agent_works = test_simple_agent()
    
    print("\n" + "=" * 50)
    if agent_works:
        print("✅ MCP tools working with simple agent!")
    else:
        print("⚠️  Agent has issues but direct tools work")