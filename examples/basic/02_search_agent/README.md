# Search-Enabled ReAct Agent

This example demonstrates a ReAct agent equipped with web search capabilities using DuckDuckGo.

## What This Example Demonstrates

- Creating a ReAct agent with search tools
- Using DuckDuckGo search for real-time information retrieval
- How agents reason about when to search vs. when to use existing knowledge
- Tool integration with LangChain agents

## How It Works

The agent can:
1. **Reason** about whether it needs to search for current information
2. **Act** by either searching the web or using its existing knowledge
3. **Observe** search results and incorporate them into its response

The search tool allows the agent to find up-to-date information that wasn't in its training data.

## Running the Example

1. Make sure Ollama is running locally on port 11434
2. Ensure the "gpt-oss:20b" model is available in Ollama
3. Install required dependencies:
   ```bash
   pip install duckduckgo-search
   ```
4. Run the example:
   ```bash
   cd examples/basic/02_search_agent
   python main.py
   ```

## Dependencies

This example requires:
- `langchain-community` for the DuckDuckGo search tool
- `duckduckgo-search` as the underlying search library

## Code Structure

- `main.py`: Creates agent with DuckDuckGo search tool
- Uses `DuckDuckGoSearchRun` from langchain-community
- Demonstrates querying for recent information

## Example Queries to Try

- "What are the latest developments in AI?"
- "Current stock price of [company]"
- "Recent news about [topic]"
- "Weather in [city] today"

## Next Steps

This example can be extended by:
- Adding multiple search tools (Google, Bing, etc.)
- Implementing search result filtering and ranking
- Adding memory to remember previous searches
- Combining search with other tools like calculators or APIs