#!/usr/bin/env python3
"""
Simple MCP Agent that works reliably without complex ReAct parsing issues
"""

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from simulated_mcp_wrapper import simulated_mcp_client
import re

class SimpleMCPAgent:
    """A simple MCP-enabled agent that avoids ReAct parsing complexity"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-oss:20b",
            api_key="ollama", 
            base_url="http://localhost:11434/v1"
        )
        self.tools = simulated_mcp_client.get_langchain_tools()
        self.tool_map = {
            "calculator_add": self.tools[0],
            "calculator_multiply": self.tools[1], 
            "web_search": self.tools[2],
            "file_read": self.tools[3],
            "file_list": self.tools[4]
        }
    
    def process_query(self, query: str):
        """Process query using direct tool selection"""
        print("🔧 SIMPLE MCP-ENABLED AGENT")
        print("=" * 70)
        print(f"Query: {query}")
        print("=" * 70)
        
        # Analyze query to select appropriate tool
        tool_choice = self._select_tool(query)
        
        if tool_choice["tool"] == "none":
            return self._direct_llm_response(query)
        else:
            return self._use_tool_and_respond(query, tool_choice)
    
    def _select_tool(self, query: str):
        """Simple rule-based tool selection"""
        query_lower = query.lower()
        
        # Calculator detection
        if any(word in query_lower for word in ["add", "plus", "+", "sum", "calculate"]) and any(char.isdigit() for char in query):
            numbers = re.findall(r'\d+', query)
            if len(numbers) >= 2:
                return {"tool": "calculator_add", "params": f"{numbers[0]}, {numbers[1]}"}
        
        if any(word in query_lower for word in ["multiply", "times", "×", "*"]) and any(char.isdigit() for char in query):
            numbers = re.findall(r'\d+', query)
            if len(numbers) >= 2:
                return {"tool": "calculator_multiply", "params": f"{numbers[0]}, {numbers[1]}"}
        
        # Search detection
        if any(word in query_lower for word in ["search", "find", "look up", "information about"]):
            return {"tool": "web_search", "params": query}
        
        # File operations
        if "list files" in query_lower or "files in" in query_lower:
            return {"tool": "file_list", "params": ""}
        
        if "read file" in query_lower or "file content" in query_lower:
            return {"tool": "file_read", "params": "/tmp/mcp_demo.txt"}
        
        return {"tool": "none", "params": None}
    
    def _use_tool_and_respond(self, query: str, tool_choice: dict):
        """Use selected tool and formulate response"""
        tool_name = tool_choice["tool"]
        params = tool_choice["params"]
        
        print(f"🔧 Selected Tool: {tool_name}")
        print(f"📝 Parameters: {params}")
        print("-" * 50)
        
        # Execute tool
        try:
            tool = self.tool_map[tool_name]
            if tool_name in ["calculator_add", "calculator_multiply", "file_list"]:
                result = tool.invoke({"input_text": params})
            elif tool_name == "web_search":
                result = tool.invoke({"query": params})
            elif tool_name == "file_read":
                result = tool.invoke({"filepath": params})
            else:
                result = "Unknown tool"
            
            print(f"🔧 Tool Result: {result}")
            print("-" * 50)
            
            # Generate natural response
            response_prompt = f"""Based on this tool result, provide a natural response to the user's query.

User Query: {query}
Tool Used: {tool_name}
Tool Result: {result}

Provide a concise, helpful response:"""
            
            messages = [
                SystemMessage(content="You are a helpful assistant. Provide clear, concise responses based on tool results."),
                HumanMessage(content=response_prompt)
            ]
            
            llm_response = self.llm.invoke(messages)
            return llm_response.content
            
        except Exception as e:
            return f"Error using tool {tool_name}: {str(e)}"
    
    def _direct_llm_response(self, query: str):
        """Direct LLM response when no tool is needed"""
        print("🧠 Using Direct LLM Response (No Tool Needed)")
        print("-" * 50)
        
        messages = [
            SystemMessage(content="You are a helpful assistant with access to MCP tools. Respond naturally to the user's query."),
            HumanMessage(content=query)
        ]
        
        response = self.llm.invoke(messages)
        return response.content

# Test the simple agent
if __name__ == "__main__":
    agent = SimpleMCPAgent()
    
    test_queries = [
        "Calculate 15 + 27",
        "What is 8 times 12?", 
        "Search for information about Python 3.13",
        "List the files in the directory",
        "What is the capital of France?"  # No tool needed
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*10} TEST QUERY {i} {'='*10}")
        result = agent.process_query(query)
        print("FINAL RESPONSE:")
        print(result)
        if i < len(test_queries):
            print("\n" + "⏸️ " * 20)