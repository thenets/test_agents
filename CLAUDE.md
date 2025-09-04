# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project that implements a LangChain-based AI agent using the ReAct (Reasoning and Acting) pattern. The main application creates an agent executor that can process user queries and provide responses using an LLM.

## Key Architecture

- **main.py**: Entry point that sets up a LangChain ReAct agent using ChatOpenAI with a local Ollama backend
- **agent-testarea/**: Python virtual environment directory (not source code)
- **requirements.txt**: Python dependencies (currently empty)

## Development Setup

1. Activate virtual environment: `source agent-testarea/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## LLM Configuration

The project is configured to use:
- Model: "gpt-oss:20b" 
- Backend: Local Ollama server at http://localhost:11434/v1
- Agent type: ReAct agent executor with hub prompt "wfh/react-agent-executor"

## Dependencies

The project uses LangChain ecosystem packages:
- langchain
- langchain-community  
- langchain-openai
- langchain-core
- langgraph