"""
Simulated MCP Wrapper for LangChain Integration

This module provides a bridge between simulated MCP functionality and LangChain tools.
It demonstrates the pattern for MCP integration without requiring real MCP servers.

NOTE: This is SIMULATED MCP functionality for educational purposes.
For real MCP integration, you would use the actual MCP Python SDK with ClientSession.
"""

import asyncio
from typing import Dict, List, Any
from langchain.tools import tool
import tempfile
import os


class SimulatedMCPWrapper:
    """
    SIMULATED MCP wrapper that provides MCP-style functionality without real MCP protocol.
    
    This class demonstrates the integration pattern between MCP-style tools and LangChain.
    In a real implementation, this would use the MCP Python SDK to communicate with
    actual MCP servers via stdio, HTTP, or other transports.
    """
    
    def __init__(self):
        self.servers = {}
        self.temp_dir = tempfile.gettempdir()
        
    def add_server(self, name: str, command: List[str]):
        """Add an MCP server configuration"""
        self.servers[name] = {
            'command': command,
            'process': None
        }
    
    async def call_simulated_mcp_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        SIMULATE calling a tool on an MCP server.
        
        In a real MCP implementation, this would:
        1. Connect to the MCP server via stdio/HTTP transport
        2. Send a call_tool request with the tool_name and arguments  
        3. Receive and return the actual MCP server response
        
        This simulation provides the same interface for educational purposes.
        """
        try:
            # SIMULATED responses - in real MCP, these would come from actual servers
            
            if server_name == "calculator" and tool_name == "add":
                a = arguments.get('a', 0)
                b = arguments.get('b', 0)
                result = a + b
                return f"Calculator result: {a} + {b} = {result}"
                
            elif server_name == "calculator" and tool_name == "multiply":
                a = arguments.get('a', 0)
                b = arguments.get('b', 0)
                result = a * b
                return f"Calculator result: {a} × {b} = {result}"
                
            elif server_name == "web_search" and tool_name == "search_web":
                query = arguments.get('query', '')
                return f"""Web search results for "{query}":

1. Example Result - Information about {query}
   This is a simulated search result from the MCP web search server.
   
2. Related Article - More details on {query}
   Additional relevant information found via MCP search.
   
3. Reference - {query} documentation
   Technical documentation and guides.

(Results from MCP Web Search Server)"""
                
            elif server_name == "file" and tool_name == "read_file":
                filepath = arguments.get('filepath', '')
                # Create a demo file for testing
                demo_path = os.path.join(self.temp_dir, "mcp_demo.txt")
                if not os.path.exists(demo_path):
                    with open(demo_path, 'w') as f:
                        f.write("This is a demo file created by the MCP File Server.\n\nIt contains sample content for testing MCP file operations.")
                
                if filepath == demo_path or filepath.endswith("mcp_demo.txt"):
                    with open(demo_path, 'r') as f:
                        content = f.read()
                    return f"File contents from MCP server:\n\n{content}"
                else:
                    return f"File not found or access denied: {filepath}"
                    
            elif server_name == "file" and tool_name == "list_files":
                files = os.listdir(self.temp_dir)[:10]  # Limit to 10 files
                file_list = "\n".join(f"- {f}" for f in files)
                return f"Files in temp directory (via MCP):\n\n{file_list}"
                
            else:
                return f"Unknown tool '{tool_name}' on server '{server_name}'"
                
        except Exception as e:
            return f"MCP call failed: {str(e)}"
    
    def get_langchain_tools(self):
        """Get LangChain tools that wrap MCP server capabilities"""
        
        @tool
        def mcp_calculator_add(input_text: str) -> str:
            """Add two numbers using MCP calculator server. Input should be 'number1, number2' or 'number1 and number2'"""
            try:
                # Parse input - handle various formats
                if ',' in input_text:
                    parts = input_text.split(',')
                elif ' and ' in input_text:
                    parts = input_text.split(' and ')
                elif ' ' in input_text:
                    parts = input_text.split()
                else:
                    return "Please provide two numbers separated by comma or space"
                
                if len(parts) != 2:
                    return f"Expected 2 numbers, got {len(parts)}: {input_text}"
                
                a = float(parts[0].strip())
                b = float(parts[1].strip())
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(
                        self.call_simulated_mcp_tool("calculator", "add", {"a": a, "b": b})
                    )
                finally:
                    loop.close()
            except Exception as e:
                return f"Error parsing input '{input_text}': {str(e)}"
        
        @tool
        def mcp_calculator_multiply(input_text: str) -> str:
            """Multiply two numbers using MCP calculator server. Input should be 'number1, number2' or 'number1 and number2'"""
            try:
                # Parse input - handle various formats
                if ',' in input_text:
                    parts = input_text.split(',')
                elif ' and ' in input_text:
                    parts = input_text.split(' and ')
                elif ' ' in input_text:
                    parts = input_text.split()
                else:
                    return "Please provide two numbers separated by comma or space"
                
                if len(parts) != 2:
                    return f"Expected 2 numbers, got {len(parts)}: {input_text}"
                
                a = float(parts[0].strip())
                b = float(parts[1].strip())
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(
                        self.call_simulated_mcp_tool("calculator", "multiply", {"a": a, "b": b})
                    )
                finally:
                    loop.close()
            except Exception as e:
                return f"Error parsing input '{input_text}': {str(e)}"
        
        @tool
        def mcp_web_search(query: str) -> str:
            """Search the web using MCP web search server"""
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(
                    self.call_simulated_mcp_tool("web_search", "search_web", {"query": query})
                )
            finally:
                loop.close()
        
        @tool
        def mcp_file_read(filepath: str) -> str:
            """Read a file using MCP file server. Provide the full file path."""
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(
                    self.call_simulated_mcp_tool("file", "read_file", {"filepath": filepath})
                )
            finally:
                loop.close()
        
        @tool  
        def mcp_file_list(input_text: str = "") -> str:
            """List files using MCP file server. No input needed - just provide empty string or 'list files'."""
            # input_text is not used but kept for consistent interface
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(
                    self.call_simulated_mcp_tool("file", "list_files", {})
                )
            finally:
                loop.close()
        
        return [
            mcp_calculator_add,
            mcp_calculator_multiply, 
            mcp_web_search,
            mcp_file_read,
            mcp_file_list
        ]


# Global instance for easy access
simulated_mcp_client = SimulatedMCPWrapper()

# Configure simulated MCP servers (these aren't actually used in simulation mode)
simulated_mcp_client.add_server("calculator", ["simulated-calculator-server"])
simulated_mcp_client.add_server("web_search", ["simulated-web-search-server"])
simulated_mcp_client.add_server("file", ["simulated-file-server"])