# Simple ReAct Agent

This is a basic example of a ReAct (Reasoning and Acting) agent using LangChain and LangGraph.

## What This Example Demonstrates

- Creating a simple ReAct agent with no tools
- Using a local Ollama backend for the LLM
- Basic agent conversation flow

## How It Works

The agent uses the ReAct pattern to:
1. **Reason** about the user's question
2. **Act** by generating a response (no external tools in this basic example)
3. **Observe** the result and continue the conversation

## Running the Example

1. Make sure Ollama is running locally on port 11434
2. Ensure the "gpt-oss:20b" model is available in Ollama
3. Run the example:

```bash
cd examples/basic/01_simple_react_agent
python main.py
```

## Code Structure

- `main.py`: The main script that creates and runs the ReAct agent
- Uses `create_react_agent` from LangGraph's prebuilt components
- Configured with ChatOpenAI pointing to local Ollama instance

## Next Steps

This basic example can be extended by:
- Adding tools for the agent to use
- Implementing memory for conversation history
- Adding custom prompts or instructions