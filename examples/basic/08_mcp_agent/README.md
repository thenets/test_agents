# MCP-Style Tool Integration Example

This example demonstrates how to integrate MCP-style tools with LangChain agents using simulated MCP functionality for educational purposes.

## What This Example Demonstrates

- **MCP Integration Pattern**: Shows how to bridge MCP-style tools with LangChain agents
- **Tool Orchestration**: Agent decides which tools to use for different queries
- **Simulated Capabilities**: Calculator, web search, and file operations
- **LangChain Bridge**: Pattern for integrating external tool protocols with LangChain
- **Educational Foundation**: Learning base for real MCP integration

## Important Note

**This is SIMULATED MCP functionality**, not real MCP protocol communication. It demonstrates the integration pattern and provides a foundation for understanding how to connect MCP tools with LangChain agents.

## Key Difference from Previous Examples

| Aspect | Previous Examples | Example 8 (Simulated MCP) |
|--------|------------------|---------------------------|
| **Tool Integration** | Direct LangChain tools | MCP-style tool wrapper pattern |
| **Architecture** | Simple tool functions | Simulated server/client architecture |
| **Capabilities** | Basic functionality | Multi-domain tools (calc, search, files) |
| **Learning Value** | LangChain basics | External protocol integration patterns |
| **Real-world Prep** | Direct usage | Foundation for MCP/other protocols |

## Architecture

### 🔧 Simulated MCP Tools

1. **Simulated Calculator**
   - **Purpose**: Mathematical computations via simulated MCP interface
   - **Tools**: add, multiply
   - **Benefits**: Demonstrates MCP-style tool integration pattern

2. **Simulated Web Search**
   - **Purpose**: Web search simulation through MCP-style interface
   - **Tools**: search_web
   - **Benefits**: Shows how to integrate search capabilities

3. **Simulated File Operations**
   - **Purpose**: File operations through simulated MCP interface
   - **Tools**: read_file, list_files
   - **Benefits**: Demonstrates secure file access patterns

### 🤖 Agent Architecture

```
User Query
    ↓
SimpleMCPAgent (GPT-OSS:20b) analyzes query
    ↓
Agent selects appropriate simulated tool:
- Math calculation needed? → Simulated Calculator
- Information lookup needed? → Simulated Web Search
- File operations needed? → Simulated File Operations
- General query? → Direct LLM response
    ↓
Simulated MCP Wrapper executes tool simulation
    ↓
Simulated results returned in MCP-style format
    ↓
Agent synthesizes natural language response
```

## Running the Example

1. Make sure Ollama is running locally on port 11434
2. Ensure required models are available:
   ```bash
   ollama pull gpt-oss:20b
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the example:
   ```bash
   cd examples/basic/08_mcp_agent
   python main.py
   ```

## Example Queries and Expected Tool Usage

### Query: "Calculate 15 + 27 using the MCP calculator"
- **Expected Tools**: MCP Calculator Server (add tool)
- **Process**: Call MCP calculator server → Execute addition → Return result
- **Benefits**: Demonstrates real MCP tool integration

### Query: "Search the web for information about Python 3.13 features"
- **Expected Tools**: MCP Web Search Server (search_web tool)
- **Process**: Call MCP web search server → Execute search → Return results
- **Benefits**: Real-time information access via MCP protocol

### Query: "List the files in the temp directory using MCP file server"
- **Expected Tools**: MCP File Server (list_files tool)
- **Process**: Call MCP file server → List directory contents → Return file list
- **Benefits**: Secure file operations through MCP interface

### Query: "Calculate 8 × 12 and then search for information about that number"
- **Expected Tools**: MCP Calculator + MCP Web Search
- **Process**: Calculate using MCP → Search for result using MCP → Combine responses
- **Benefits**: Demonstrates chaining multiple MCP servers

## MCP Tool Implementation

### Real MCP Integration
This example now uses actual MCP servers through the MCP Python SDK:

- **MCP Servers**: Three separate MCP servers (`calculator_server.py`, `web_search_server.py`, `file_server.py`)
- **Client Wrapper**: `mcp_client_wrapper.py` bridges MCP servers with LangChain tools
- **Protocol Compliance**: Uses real MCP protocol for tool calls and responses

### Architecture Components

```python
# MCP Client Wrapper Integration
from mcp_client_wrapper import mcp_client

# Get LangChain tools that wrap MCP servers
tools = mcp_client.get_langchain_tools()

# Each tool calls real MCP servers via the wrapper
@tool
def mcp_calculator_add(a: float, b: float) -> str:
    """Add two numbers using MCP calculator server"""
    return mcp_client.call_mcp_tool("calculator", "add", {"a": a, "b": b})
```

## Benefits of MCP Integration

### Expanded Capabilities
- **Real-time Information**: Access to current web content
- **Current Documentation**: Latest library docs and API references
- **Dynamic Knowledge**: Information beyond training data limitations

### Practical Applications
- **Development Assistance**: Get latest framework documentation
- **Research Tasks**: Fetch current information on any topic  
- **API Integration**: Access to external services and data sources
- **Content Analysis**: Process and analyze web content

### Tool Orchestration
- **Intelligent Selection**: Agent chooses appropriate tools for each query
- **Tool Chaining**: Combine multiple MCP tools for complex tasks
- **Error Recovery**: Graceful handling of tool failures

## Code Structure

- `MCPAgent`: Main agent class with MCP tool integration
- `create_web_fetch_tool()`: Web content retrieval tool
- `create_context7_resolve_tool()`: Library ID resolution tool  
- `create_context7_docs_tool()`: Documentation retrieval tool
- `process_query()`: End-to-end query processing with tool orchestration

## Extending the Example

This example can be expanded with:

### Additional MCP Tools
- **Database Tools**: Query databases through MCP
- **API Integration Tools**: Access external APIs
- **File Processing Tools**: Handle documents and files
- **Communication Tools**: Email, messaging integration

### Enhanced Agent Capabilities  
- **Multi-step Planning**: Complex task decomposition
- **Tool Result Caching**: Avoid redundant tool calls
- **User Preference Learning**: Adapt tool selection over time
- **Parallel Tool Execution**: Execute multiple tools simultaneously

### Real-world Integration
- **Production MCP Setup**: Connect to actual MCP servers
- **Authentication**: Handle API keys and authentication
- **Rate Limiting**: Respect tool usage limits
- **Monitoring**: Track tool usage and performance

## Performance Considerations

### Tool Selection Efficiency
- **Smart Routing**: Only use tools when necessary
- **Tool Combination**: Efficient chaining of related tools
- **Fallback Strategies**: Handle tool failures gracefully

### Response Quality
- **Information Synthesis**: Combine multiple tool results effectively
- **Source Attribution**: Track information sources
- **Freshness Indicators**: Show when information was retrieved

## Next Steps

This foundational MCP example demonstrates the power of extending agents with external tools. Future examples could explore:

- **Specialized MCP Workflows**: Domain-specific tool chains
- **Multi-Agent MCP Systems**: Agents sharing MCP resources
- **Custom MCP Tools**: Building your own MCP protocol tools
- **Production Deployment**: Scaling MCP-enabled agents