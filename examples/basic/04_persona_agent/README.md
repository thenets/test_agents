# Persona Agent - Dr. Code

This example demonstrates how to add a persona to an AI agent using system prompts, dramatically changing the agent's response style and personality.

## What This Example Demonstrates

- **Persona Implementation**: Using system messages to define agent personality
- **Response Style Changes**: How personas affect tone, structure, and content
- **System Prompting**: Practical application of system-level instructions
- **Comparison Testing**: Side-by-side comparison of responses with/without persona

## The Dr. Code Persona

**Dr. Code** is a friendly, enthusiastic computer science professor with these traits:

- **Warm and encouraging**: Patient, supportive teaching approach
- **Educational focus**: Clear explanations with helpful analogies  
- **Mentoring style**: Makes complex concepts approachable
- **Positive reinforcement**: Always ends with encouragement or tips

## How It Works

The example uses LangChain's `SystemMessage` to establish the persona before processing user queries:

1. **System Message**: Defines Dr. Code's personality and teaching style
2. **User Query**: Processes the question through the persona lens
3. **Comparison**: Shows responses both with and without the persona

## Running the Example

1. Make sure Ollama is running locally on port 11434
2. Ensure the "gpt-oss:20b" model is available in Ollama
3. Run the example:
   ```bash
   cd examples/basic/04_persona_agent
   python main.py
   ```

## Test Query

The example uses a simple programming question:
> "What is a function in Python?"

This question is ideal for demonstrating how a teaching persona affects the response style, structure, and educational approach.

## Expected Differences

### Without Persona
- Direct, technical explanation
- Factual but potentially dry
- Standard formatting

### With Dr. Code Persona  
- Warm, encouraging tone
- Educational analogies and examples
- Supportive language and encouragement
- More engaging and approachable explanation

## Code Structure

- `dr_code_persona`: String defining the persona characteristics
- `run_without_persona()`: Processes query with no system message
- `run_with_persona()`: Processes query with Dr. Code persona
- Side-by-side comparison output

## Customization Ideas

### Creating New Personas

```python
# Professional Business Analyst
business_persona = """You are a senior business analyst who:
- Speaks formally and professionally
- Focuses on practical applications
- Uses business terminology
- Provides structured, actionable insights"""

# Witty Comedy Writer  
comedy_persona = """You are a witty comedian who:
- Uses humor and clever wordplay
- Makes light of technical topics
- Uses entertaining analogies
- Keeps responses fun and engaging"""
```

### Different Query Types

Test your personas with various query types:
- **Technical questions**: "How does recursion work?"
- **Creative prompts**: "Write a story about debugging"
- **Problem-solving**: "My code isn't working, help!"
- **Explanations**: "What is machine learning?"

## Next Steps

This basic persona example can be extended with:
- **Multiple personas**: Switch between different personalities
- **Contextual personas**: Choose persona based on query type
- **Persona persistence**: Maintain personality across conversation
- **Dynamic personas**: Modify personality traits on the fly
- **User preferences**: Let users select their preferred teaching style