# AI Agent Examples

A collection of standalone examples demonstrating different types of AI agents using LangChain, LangGraph, and various LLM providers including local Ollama and OpenRouter.

## Prerequisites

1. **Ollama**: Install and run Ollama locally
   ```bash
   # Install Ollama (see https://ollama.ai)
   # Pull the required models
   ollama pull gpt-oss:20b
   ollama pull mistral
   ollama pull gemma3:1b
   ```

2. **Python Dependencies**: Install required packages
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
├── examples/basic/          # Basic agent examples
│   ├── 01_simple_react_agent/    # Basic ReAct agent with no tools
│   ├── 02_search_agent/          # ReAct agent with web search
│   ├── 03_controller_agent/      # Controller agent with dual LLM routing
│   ├── 04_persona_agent/         # Agent with Dr. Code teaching persona
│   ├── 05_multi_persona_controller/  # Advanced controller with 4 persona+LLM combinations
│   ├── 06_multi_agent_critique/  # Multi-agent system with solver and judge collaboration
│   ├── 07_agent_controller/      # AI-powered agent selection with reasoning
│   └── 08_mcp_agent/             # Simulated MCP tool integration
├── examples/langgraph/      # LangGraph-focused examples
│   ├── 01_structured_output_openrouter/  # Structured output with OpenRouter integration
│   ├── 02_tool_integration_calculator/   # ReAct agent with calculator tools
│   └── 03_simple_agent_loop/             # Basic agent loop pattern with plan-act-observe cycle
```

## Examples

### Basic Examples

1. **[Simple ReAct Agent](examples/basic/01_simple_react_agent/)**
   - Basic ReAct pattern implementation
   - No external tools
   - Demonstrates core agent reasoning

2. **[Search-Enabled Agent](examples/basic/02_search_agent/)**
   - ReAct agent with DuckDuckGo search
   - Real-time information retrieval
   - Tool integration example

3. **[Controller Agent](examples/basic/03_controller_agent/)**
   - Intelligent routing between multiple LLMs
   - Keyword-based model selection (GPT-OSS:20b vs Mistral)
   - Demonstrates multi-model orchestration

4. **[Persona Agent](examples/basic/04_persona_agent/)**
   - Agent with "Dr. Code" teaching persona
   - System prompting for personality and response style
   - Side-by-side comparison of responses with/without persona

5. **[Multi-Persona Controller](examples/basic/05_multi_persona_controller/)**
   - Advanced controller with 4 persona+LLM combinations
   - Dr. Code (GPT-OSS), Creative Writer (Mistral), Business Analyst (GPT-OSS), Witty Comedian (Mistral)
   - Intelligent routing based on query content and optimal model selection

6. **[Multi-Agent Critique System](examples/basic/06_multi_agent_critique/)**
   - Collaborative solver and judge agents working together
   - Iterative improvement through critique and feedback loops
   - Quality control with automated response evaluation and refinement

7. **[Agent-Based Controller](examples/basic/07_agent_controller/)**
   - AI-powered routing with Mistral controller agent
   - Intelligent agent selection based on reasoning rather than keywords
   - Mixed model strategy for optimal speed/quality balance

8. **[Simulated MCP Agent](examples/basic/08_mcp_agent/)**
   - Agent with simulated Model Context Protocol (MCP) tool integration
   - Calculator, web search simulation, and file operations
   - Educational example of MCP-style tool integration patterns
   - Demonstrates LangChain bridge pattern for external tool protocols

### LangGraph Examples

9. **[Structured Output with OpenRouter](examples/langgraph/01_structured_output_openrouter/)**
   - LangGraph StateGraph with conditional routing between specialized agents
   - Structured output using Pydantic models (WeatherResponse, TaskAnalysisResponse, PersonResponse)
   - OpenRouter integration for multi-provider LLM access
   - Demonstrates weather queries, task analysis, and biographical information extraction

10. **[Tool Integration with Calculator](examples/langgraph/02_tool_integration_calculator/)**
    - LangGraph ReAct agent with custom tool integration
    - Calculator tools using @tool decorator (add, subtract, multiply, divide)
    - Automatic tool selection and execution flow visualization
    - Demonstrates basic mathematical operations and error handling

11. **[Simple Agent Loop](examples/langgraph/03_simple_agent_loop/)**
    - Fundamental agent pattern: plan → act → observe → repeat
    - Natural exit strategy when no more tool calls needed
    - Multi-step reasoning and state accumulation through iterations
    - Clear demonstration of core agent loop mechanics

## Running Examples

Each example is self-contained and can be run independently:

```bash
# Run simple ReAct agent
cd examples/basic/01_simple_react_agent
python main.py

# Run search-enabled agent
cd examples/basic/02_search_agent
python main.py

# Run controller agent
cd examples/basic/03_controller_agent
python main.py

# Run persona agent
cd examples/basic/04_persona_agent
python main.py

# Run multi-persona controller
cd examples/basic/05_multi_persona_controller
python main.py

# Run multi-agent critique system
cd examples/basic/06_multi_agent_critique
python main.py

# Run agent-based controller
cd examples/basic/07_agent_controller
python main.py

# Run simulated MCP agent
cd examples/basic/08_mcp_agent
python main.py

# Run structured output with OpenRouter
cd examples/langgraph/01_structured_output_openrouter
python main.py

# Run calculator tool integration
cd examples/langgraph/02_tool_integration_calculator
python main.py

# Run simple agent loop
cd examples/langgraph/03_simple_agent_loop
python main.py
```

## Configuration

### LLM Setup

**Basic Examples** use local Ollama by default:
- **Models**: gpt-oss:20b, mistral, gemma3:1b (examples use different combinations)
- **API**: Local Ollama at http://localhost:11434/v1
- **API Key**: "ollama" (placeholder for Ollama)

**LangGraph Examples** support multiple providers:
- **OpenRouter**: Access to 200+ models from various providers (requires API key)
- **Local Ollama**: Compatible with local models for development
- Configuration via environment variables in each example

## Adding New Examples

1. Create a new directory under `examples/basic/` (or appropriate category)
2. Add `main.py` with your agent implementation
3. Include a `README.md` explaining the example
4. Update this main README with the new example

## Dependencies

Core dependencies used across examples:
- `langchain`: Core LangChain framework
- `langchain-community`: Community tools and integrations
- `langchain-openai`: OpenAI-compatible LLM interface
- `langgraph`: Graph-based agent framework
- `pydantic`: Data validation and structured output models
- `python-dotenv`: Environment variable management

See `requirements.txt` for the complete list.

## Contributing

When adding new examples:
- Follow the existing directory structure
- Include comprehensive README files
- Test with the default Ollama setup