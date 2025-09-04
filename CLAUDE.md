# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of standalone AI agent examples using LangChain, LangGraph, and local Ollama models. The project demonstrates different agent patterns and capabilities through organized, self-contained examples.

## Project Structure

- **examples/**: Organized agent examples by complexity level
  - **basic/**: Fundamental agent patterns
    - **01_simple_react_agent/**: Basic ReAct agent with no tools
    - **02_search_agent/**: ReAct agent with web search capabilities
- **shared/**: Common utilities and configurations
  - **llm_config.py**: Shared LLM configuration utilities
- **agent-testarea/**: Python virtual environment directory (not source code)
- **requirements.txt**: Python dependencies for all examples

## Development Setup

1. Activate virtual environment: `source agent-testarea/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure Ollama is running: Check http://localhost:11434
4. Run any example: `cd examples/basic/[example-name] && python main.py`

## LLM Configuration

All examples use shared configuration:
- Model: "gpt-oss:20b" 
- Backend: Local Ollama server at http://localhost:11434/v1
- Shared utilities in `shared/llm_config.py`

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