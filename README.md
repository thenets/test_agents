# AI Agent Examples

A collection of standalone examples demonstrating different types of AI agents using LangChain, LangGraph, and local Ollama models.

## Prerequisites

1. **Ollama**: Install and run Ollama locally
   ```bash
   # Install Ollama (see https://ollama.ai)
   # Pull the required models
   ollama pull gpt-oss:20b
   ollama pull mistral
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
│   └── 04_persona_agent/         # Agent with Dr. Code teaching persona
├── shared/                  # Common utilities and configurations
└── docs/                    # Additional documentation
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
```

## Configuration

### LLM Setup
All examples use local Ollama by default:

- **Models**: gpt-oss:20b, mistral (controller agent uses both)
- **API**: Local Ollama at http://localhost:11434/v1
- **API Key**: "ollama" (placeholder for Ollama)

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

See `requirements.txt` for the complete list.

## Contributing

When adding new examples:
- Follow the existing directory structure
- Include comprehensive README files
- Use the shared utilities where possible
- Test with the default Ollama setup