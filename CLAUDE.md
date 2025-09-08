# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of standalone AI agent examples using LangChain, LangGraph, and various LLM providers including local Ollama and OpenRouter. The project demonstrates different agent patterns and capabilities through organized, self-contained examples.

## Project Structure

- **examples/**: Organized agent examples by category
  - **basic/**: Fundamental agent patterns using local Ollama
    - **01_simple_react_agent/**: Basic ReAct agent with no tools
    - **02_search_agent/**: ReAct agent with web search capabilities
    - **03_controller_agent/**: Controller agent with dual LLM routing
    - **04_persona_agent/**: Agent with Dr. Code teaching persona
    - **05_multi_persona_controller/**: Advanced controller with 4 persona+LLM combinations
    - **06_multi_agent_critique/**: Multi-agent system with solver and judge collaboration
    - **07_agent_controller/**: AI-powered agent selection with reasoning
    - **08_mcp_agent/**: Simulated MCP tool integration
  - **langgraph/**: LangGraph-focused examples with multiple LLM providers
    - **01_structured_output_openrouter/**: Structured output with OpenRouter integration
- **agent-testarea/**: Python virtual environment directory (not source code)
- **requirements.txt**: Python dependencies for all examples

## Development Setup

1. Activate virtual environment: `source agent-testarea/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure Ollama is running: Check http://localhost:11434
4. Run any example: `cd examples/[category]/[example-name] && python main.py`

## LLM Configuration

**Basic Examples** use local Ollama:
- Model: "gpt-oss:20b", "mistral", "gemma3:1b"
- Backend: Local Ollama server at http://localhost:11434/v1
- API Key: "ollama" (placeholder)

**LangGraph Examples** support multiple providers:
- OpenRouter: Multiple providers via https://openrouter.ai/api/v1 (requires API key)
- Local Ollama: Compatible with local models for development
- Configuration via environment variables (.env files)

## Adding New Examples

When creating new examples:
1. Follow the directory structure: `examples/[category]/[number]_[name]/`
2. Include main.py and README.md in each example
3. Use shared utilities from `shared/` where possible
4. Update main README.md with new example descriptions

## Dependencies

Core packages used across examples:
- langchain: Core framework
- langchain-community: Tools and integrations
- langchain-openai: OpenAI-compatible interface
- langgraph: Graph-based agents
- duckduckgo-search: For search-enabled examples
- pydantic: Data validation and structured output models
- python-dotenv: Environment variable management