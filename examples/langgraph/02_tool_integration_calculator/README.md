# LangGraph Tool Integration with Calculator

This example demonstrates how to integrate custom tools with LangGraph agents using a basic calculator as a practical example. The agent can perform mathematical operations (+, -, *, /) using dedicated tools rather than attempting calculations directly.

## Features

- **Custom Tool Creation**: Define tools using the `@tool` decorator from LangChain
- **ReAct Agent Pattern**: LangGraph's `create_react_agent` with tool calling capabilities
- **Automatic Tool Selection**: Agent intelligently chooses appropriate tools for calculations
- **Error Handling**: Proper error handling for edge cases (e.g., division by zero)
- **Execution Visualization**: Detailed view of tool calls and execution flow
- **Multiple LLM Support**: Works with OpenRouter and local Ollama

## Setup

1. **Install Dependencies**
   ```bash
   # From the project root
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cd examples/langgraph/02_tool_integration_calculator
   cp .env.example .env
   ```

3. **Set API Key (Optional)**
   - For OpenRouter: Get your API key from [OpenRouter](https://openrouter.ai/keys)
   - Edit `.env` and set your `OPENROUTER_API_KEY`
   - If no API key is provided, it will fall back to local Ollama

4. **Choose Your Model**
   - Edit `MODEL_NAME` in `.env` for your preferred model
   - Recommended for tool calling: `deepseek/deepseek-chat`, `anthropic/claude-3-haiku`, `openai/gpt-4o-mini`

## How It Works

### 1. Tool Definition (`tools.py`)

Tools are defined using the `@tool` decorator with proper type hints and documentation:

```python
from langchain_core.tools import tool

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together.
    
    Args:
        a: First number to add
        b: Second number to add
        
    Returns:
        The sum of a and b
    """
    return a + b
```

Each tool includes:
- **Clear function signature** with type hints
- **Comprehensive docstring** that helps the LLM understand when to use the tool
- **Error handling** for edge cases (like division by zero)

### 2. Agent Creation (`main.py`)

The ReAct agent is created using LangGraph's prebuilt function:

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    llm, 
    tools,
    system_message="You are a helpful calculator assistant..."
)
```

### 3. Tool Execution Flow

When you ask "Calculate 145 + 237", the agent:

1. **Analyzes the query** and identifies it needs to perform addition
2. **Selects the `add` tool** from available tools
3. **Extracts arguments** (145, 237) from the user query
4. **Calls the tool** with the extracted arguments
5. **Receives the result** (382) from the tool
6. **Formats the response** for the user

## Running the Example

```bash
cd examples/langgraph/02_tool_integration_calculator
python main.py
```

## Example Output

### Simple Calculation
```
==============================================================
QUERY: Calculate 145 + 237
==============================================================

🔧 Tool Calls from agent:
   Tool: add
   Args: {'a': 145, 'b': 237}
   ID: call_abc123

✅ Tool Result:
   Tool: add
   Result: 382

🤖 AI Response from agent:
   The result of 145 + 237 is 382.

🎯 FINAL ANSWER: The result of 145 + 237 is 382.

⏱️  Execution time: 1.23 seconds
==============================================================
```

### Complex Calculation
```
==============================================================
QUERY: I need to calculate (15 + 25) * 3. Can you help me with this step by step?
==============================================================

🔧 Tool Calls from agent:
   Tool: add
   Args: {'a': 15, 'b': 25}
   ID: call_def456

✅ Tool Result:
   Tool: add
   Result: 40

🔧 Tool Calls from agent:
   Tool: multiply
   Args: {'a': 40, 'b': 3}
   ID: call_ghi789

✅ Tool Result:
   Tool: multiply
   Result: 120

🤖 AI Response from agent:
   I'll solve this step by step:
   1. First, I'll calculate 15 + 25 = 40
   2. Then, I'll multiply 40 * 3 = 120
   
   The final result of (15 + 25) * 3 is 120.

🎯 FINAL ANSWER: The final result of (15 + 25) * 3 is 120.
==============================================================
```

## Available Tools

| Tool | Description | Arguments | Example |
|------|-------------|-----------|---------|
| `add` | Addition | `a: float, b: float` | `add(5, 3)` → `8` |
| `subtract` | Subtraction | `a: float, b: float` | `subtract(10, 4)` → `6` |
| `multiply` | Multiplication | `a: float, b: float` | `multiply(6, 7)` → `42` |
| `divide` | Division | `a: float, b: float` | `divide(15, 3)` → `5.0` |

### Error Handling

The tools include proper error handling:

```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Test Queries

The example includes various test cases to demonstrate tool usage:

- **Basic Operations**: "Calculate 145 + 237"
- **Word Problems**: "What is 23 * 67?"
- **Decimal Numbers**: "What is 15.5 + 24.3?"
- **Complex Expressions**: "(15 + 25) * 3"

## Key Concepts

### 1. **Tool Definition Best Practices**

- Use descriptive function names
- Include comprehensive docstrings
- Add proper type hints
- Handle edge cases gracefully
- Keep tools focused on single operations

### 2. **ReAct Pattern**

The ReAct (Reasoning + Acting) pattern allows the agent to:
- **Reason** about what tools are needed
- **Act** by calling the appropriate tools
- **Observe** the results
- **Repeat** until the task is complete

### 3. **Tool Selection**

The LLM automatically selects tools based on:
- Function names and descriptions
- Docstring content
- Input/output schemas
- Context from the user query

## Extending the Example

### Add New Mathematical Operations

1. **Define the tool**:
   ```python
   @tool
   def power(base: float, exponent: float) -> float:
       """Raise base to the power of exponent."""
       return base ** exponent
   ```

2. **Add to tool list**:
   ```python
   def get_calculator_tools():
       return [add, subtract, multiply, divide, power]
   ```

### Add Input Validation

```python
@tool
def sqrt(number: float) -> float:
    """Calculate the square root of a number."""
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return number ** 0.5
```

### Add Complex Operations

```python
@tool
def percentage(part: float, whole: float) -> float:
    """Calculate what percentage 'part' is of 'whole'."""
    if whole == 0:
        raise ValueError("Cannot calculate percentage when whole is zero")
    return (part / whole) * 100
```

## Troubleshooting

### Common Issues

1. **Tools Not Being Called**
   - Check that your model supports tool calling
   - Ensure tool descriptions are clear and specific
   - Try models specifically good at tool use (Claude, GPT-4, etc.)

2. **Incorrect Arguments**
   - Verify type hints match expected inputs
   - Check docstring parameter descriptions
   - Test with explicit numerical values

3. **Model Configuration**
   - Ensure your `.env` file is properly configured
   - Check that the selected model is available
   - Verify API keys have sufficient credits

4. **Division by Zero**
   - The `divide` tool includes error handling for this case
   - The agent should gracefully handle and report such errors

## Next Steps

- Explore more complex tool interactions
- Add tools that call external APIs
- Implement tools with memory/state
- Create multi-step workflows with tool dependencies
- Add tools for different domains (text processing, data analysis, etc.)