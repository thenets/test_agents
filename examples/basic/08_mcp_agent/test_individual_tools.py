#!/usr/bin/env python3
"""
Test individual MCP tools to identify and fix errors
"""
import os
import tempfile

def test_calculator_tools():
    """Test MCP calculator tools"""
    print("🧮 Testing Calculator Tools")
    print("-" * 30)
    
    try:
        from simulated_mcp_wrapper import simulated_mcp_client
        tools = simulated_mcp_client.get_langchain_tools()
        
        # Test calculator add
        print("Testing calculator add...")
        calc_add = tools[0]  # mcp_calculator_add
        result = calc_add.invoke({"input_text": "10, 5"})
        print(f"✅ Add result: {result}")
        
        # Test calculator multiply
        print("Testing calculator multiply...")
        calc_mult = tools[1]  # mcp_calculator_multiply
        result = calc_mult.invoke({"input_text": "6, 7"})
        print(f"✅ Multiply result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Calculator error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_web_search_tools():
    """Test MCP web search tools"""
    print("\n🌐 Testing Web Search Tools")
    print("-" * 30)
    
    try:
        from simulated_mcp_wrapper import simulated_mcp_client
        tools = simulated_mcp_client.get_langchain_tools()
        
        # Test web search
        print("Testing web search...")
        web_search = tools[2]  # mcp_web_search
        result = web_search.invoke({"query": "test query"})
        print(f"✅ Search result: {result[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Web search error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_file_tools():
    """Test MCP file tools"""
    print("\n📁 Testing File Tools")
    print("-" * 30)
    
    try:
        from simulated_mcp_wrapper import simulated_mcp_client
        tools = simulated_mcp_client.get_langchain_tools()
        
        # Test file list
        print("Testing file list...")
        file_list = tools[4]  # mcp_file_list
        result = file_list.invoke({"input_text": ""})
        print(f"✅ File list result: {result[:100]}...")
        
        # Test file read
        print("Testing file read...")
        file_read = tools[3]  # mcp_file_read  
        demo_file = os.path.join(tempfile.gettempdir(), "mcp_demo.txt")
        result = file_read.invoke({"filepath": demo_file})
        print(f"✅ File read result: {result[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ File tools error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_import_dependencies():
    """Test that all required dependencies are available"""
    print("📦 Testing Dependencies")
    print("-" * 30)
    
    try:
        print("Testing LangChain imports...")
        from langchain_openai import ChatOpenAI
        from langchain.agents import create_react_agent, AgentExecutor
        from langchain import hub
        from langchain.tools import tool
        print("✅ LangChain imports working")
        
        print("Testing MCP imports...")
        # Note: These may fail if MCP isn't installed yet
        try:
            import mcp
            print("✅ MCP package available")
        except ImportError:
            print("⚠️  MCP package not installed yet")
        
        print("Testing basic Python modules...")
        import asyncio
        import tempfile
        import os
        print("✅ Basic modules working")
        
        return True
        
    except Exception as e:
        print(f"❌ Dependency error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Individual MCP Tools Testing")
    print("=" * 50)
    
    # Test dependencies first
    deps_ok = test_import_dependencies()
    
    if deps_ok:
        # Test each tool type
        calc_ok = test_calculator_tools()
        search_ok = test_web_search_tools()
        file_ok = test_file_tools()
        
        print("\n" + "=" * 50)
        print("SUMMARY:")
        print(f"Dependencies: {'✅' if deps_ok else '❌'}")
        print(f"Calculator: {'✅' if calc_ok else '❌'}")
        print(f"Web Search: {'✅' if search_ok else '❌'}")
        print(f"File Tools: {'✅' if file_ok else '❌'}")
        
        if all([deps_ok, calc_ok, search_ok, file_ok]):
            print("\n🎉 All tools working correctly!")
        else:
            print("\n⚠️  Some tools have issues - check errors above")
    else:
        print("\n❌ Dependency issues prevent tool testing")