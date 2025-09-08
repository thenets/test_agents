# LangGraph Structured Output with OpenRouter

This example demonstrates how to use LangGraph with OpenRouter to create agents that return structured, validated output using Pydantic models.

## Features

- **OpenRouter Integration**: Connect to multiple LLM providers through a unified API
- **Structured Output**: Use Pydantic models to enforce output schemas
- **LangGraph Workflows**: Implement graph-based agent routing and processing
- **Multiple Agent Types**: Weather, task analysis, and person information agents
- **Error Handling**: Robust error handling and validation

## Setup

1. **Install Dependencies**
   ```bash
   # From the project root
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cd examples/langgraph/01_structured_output_openrouter
   cp .env.example .env
   ```

3. **Set OpenRouter API Key**
   - Get your API key from [OpenRouter](https://openrouter.ai/keys)
   - Edit `.env` and set your `OPENROUTER_API_KEY`

4. **Choose Your Model**
   - Edit `MODEL_NAME` in `.env` to select your preferred model
   - Popular options: `anthropic/claude-3-haiku`, `openai/gpt-4o-mini`, `meta-llama/llama-3.2-3b-instruct`

## How It Works

### 1. Structured Models (`models.py`)

The example defines several Pydantic models for different types of structured output:

```python
class WeatherResponse(BaseModel):
    location: str
    condition: WeatherCondition  # Enum: sunny, cloudy, rainy, etc.
    temperature: int
    humidity: Optional[int]
    description: str
```

### 2. LangGraph Workflow (`main.py`)

The main workflow uses LangGraph's `StateGraph` to:

1. **Route Queries**: Automatically determine which agent to use based on keywords
2. **Process with Structured Output**: Each agent uses `.with_structured_output()` to enforce schema
3. **Return Validated Data**: All responses are validated Pydantic objects

### 3. Agent Nodes

Three specialized agent nodes handle different query types:

- **Weather Agent**: Processes weather-related queries
- **Task Analysis Agent**: Breaks down projects into structured task lists
- **Person Info Agent**: Provides structured biographical information

## Running the Example

```bash
cd examples/langgraph/01_structured_output_openrouter
python main.py
```

## Example Output

### Weather Query
```
Query: What's the weather like in San Francisco today?
==================================================
STRUCTURED OUTPUT
==================================================
Location: San Francisco
Condition: cloudy
Temperature: 65°F
Humidity: 72%
Description: Partly cloudy with mild temperatures
==================================================
```

### Task Analysis Query
```
Query: I need to plan a website redesign project. Can you break it down into tasks?
==================================================
STRUCTURED OUTPUT
==================================================
Project: Website Redesign Project
Total Tasks: 5
Estimated Completion: 4-6 weeks

Tasks:
  1. Research and Analysis (high)
     Conduct user research and analyze current website performance
     Estimated: 16.0 hours

  2. Design Mockups (high)
     Create wireframes and visual designs for new website
     Estimated: 24.0 hours
     
... (more tasks)

Recommendations:
  • Start with user research to understand current pain points
  • Involve stakeholders in the design review process
==================================================
```

## Key Benefits

### 1. **Reliable Data Structure**
- Pydantic validation ensures consistent output format
- Type hints provide IDE support and documentation
- Enum fields prevent invalid values

### 2. **Flexible Routing**
- Automatic agent selection based on query content
- Easy to extend with new agent types
- Conditional logic handles edge cases

### 3. **OpenRouter Advantages**
- Access to 200+ models from different providers
- Automatic fallbacks and load balancing
- Cost optimization across providers
- No need to manage multiple API keys

## Extending the Example

### Add New Agent Types

1. **Define Pydantic Model**
   ```python
   class CodeAnalysisResponse(BaseModel):
       language: str
       complexity_score: int
       suggestions: List[str]
   ```

2. **Create Agent Node**
   ```python
   def code_analysis_node(state: AgentState):
       llm = configure_llm()
       structured_llm = llm.with_structured_output(CodeAnalysisResponse)
       # ... implementation
   ```

3. **Update Routing Logic**
   ```python
   def route_query(state: AgentState):
       user_message = state["messages"][-1].content.lower()
       if "code" in user_message or "programming" in user_message:
           return "code_analysis_agent"
       # ... existing logic
   ```

### Customize Models

- Add optional fields with `Optional[Type]`
- Use `Field()` for better descriptions and validation
- Create nested models for complex data structures
- Add custom validators with `@validator` decorators

## Troubleshooting

### Common Issues

1. **Missing API Key**
   - Ensure `.env` file exists and contains valid `OPENROUTER_API_KEY`
   - Check that the key has sufficient credits

2. **Model Not Available**
   - Verify the model name in your `.env` file
   - Check [OpenRouter models list](https://openrouter.ai/models) for availability

3. **Structured Output Errors**
   - Some models may not support structured output well
   - Try switching to a more capable model like Claude or GPT-4

4. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Activate your virtual environment if using one

## Next Steps

- Explore more complex LangGraph patterns with memory and persistence
- Add tool calling capabilities to your agents
- Implement streaming responses for better user experience
- Connect to external APIs and data sources