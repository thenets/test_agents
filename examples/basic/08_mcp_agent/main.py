"""
MCP-Style Tool Integration Example

This example demonstrates how to integrate MCP-style tools with LangChain agents.
Note: This uses simulated MCP functionality for educational purposes.
"""

from simple_mcp_agent import SimpleMCPAgent

def main():
    """Demonstrate MCP-style tool integration with LangChain"""
    print("🔧 MCP-STYLE TOOL INTEGRATION EXAMPLE")
    print("=" * 70)
    print("This example demonstrates simulated MCP functionality")
    print("integrated with LangChain agents for educational purposes.")
    print("=" * 70)
    
    # Create the MCP-style agent
    agent = SimpleMCPAgent()
    
    # Test queries demonstrating MCP-style capabilities
    test_queries = [
        "Calculate 15 + 27",
        "What is 8 times 12?", 
        "Search for information about Python 3.13",
        "List the files in the directory"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*10} TEST QUERY {i} {'='*10}")
        result = agent.process_query(query)
        print("FINAL RESPONSE:")
        print(result)
        if i < len(test_queries):
            print("\n" + "⏸️ " * 20)

if __name__ == "__main__":
    main()