# Multi-Persona Controller Agent

This example demonstrates an advanced controller that routes queries to 4 different persona+LLM combinations, showcasing both personality and model selection based on query analysis.

## What This Example Demonstrates

- **Advanced Agent Orchestration**: 4 specialized agents with unique persona+LLM pairings
- **Dual Routing Logic**: Selection based on both content type AND optimal model
- **Persona Specialization**: Each agent optimized for specific query types
- **Transparent Decision Making**: Clear reasoning for routing choices

## The 4 Persona+LLM Agents

### 1. Dr. Code (GPT-OSS:20b) 
- **Specialty**: Technical/Programming queries
- **Personality**: Friendly CS professor, encouraging, educational
- **Triggers**: code, programming, algorithm, debug, technical
- **Best for**: Coding help, technical explanations, software development

### 2. Creative Writer (Mistral)
- **Specialty**: Creative/Artistic content
- **Personality**: Imaginative storyteller, expressive, artistic
- **Triggers**: story, creative, poem, narrative, fiction, literature  
- **Best for**: Creative writing, storytelling, artistic content

### 3. Business Analyst (GPT-OSS:20b)
- **Specialty**: Professional/Business queries
- **Personality**: Formal, data-driven, structured, professional
- **Triggers**: business, strategy, market, revenue, corporate
- **Best for**: Business analysis, strategy, professional advice

### 4. Witty Comedian (Mistral)
- **Specialty**: Entertainment/Humor
- **Personality**: Clever, humorous, entertaining, playful
- **Triggers**: funny, joke, humor, comedy, entertaining, fun
- **Best for**: Jokes, amusing explanations, lighthearted content

## How Routing Works

The controller uses keyword-based scoring:

1. **Analyze Query**: Scan for keywords associated with each persona
2. **Calculate Scores**: Count keyword matches for each agent
3. **Select Winner**: Choose agent with highest score
4. **Default Fallback**: Use Dr. Code for neutral/tied queries
5. **Execute**: Route to selected persona+LLM combination

## Running the Example

1. Make sure Ollama is running locally on port 11434
2. Ensure both models are available:
   ```bash
   ollama pull gpt-oss:20b
   ollama pull mistral
   ```
3. Run the example:
   ```bash
   cd examples/basic/05_multi_persona_controller
   python main.py
   ```

## Example Routing Scenarios

| Query | Expected Agent | Model | Reasoning |
|-------|---------------|-------|-----------|
| "How do I implement binary search?" | Dr. Code | GPT-OSS:20b | Technical keywords detected |
| "Write a story about a dragon" | Creative Writer | Mistral | Creative keywords detected |
| "What's the best market strategy?" | Business Analyst | GPT-OSS:20b | Business keywords detected |
| "Tell me a programming joke" | Witty Comedian | Mistral | Humor keywords detected |
| "Explain machine learning" | Dr. Code | GPT-OSS:20b | Neutral query, default routing |

## Architecture Benefits

### Model Optimization
- **GPT-OSS:20b**: Used for technical and analytical tasks requiring precision
- **Mistral**: Used for creative and entertaining content requiring flair

### Persona Specialization  
- Each agent optimized for specific interaction styles
- Consistent personality maintained within domains
- Natural language experience tailored to query type

### Scalable Design
- Easy to add new persona+LLM combinations
- Modular routing logic
- Transparent decision process

## Code Structure

- `MultiPersonaController`: Main controller class
- `agents`: Dictionary defining 4 persona+LLM combinations
- `route_query()`: Keyword-based routing logic
- `process_query()`: End-to-end query processing
- Comprehensive test suite with diverse queries

## Customization Options

### Adding New Personas

```python
"data_scientist": {
    "name": "Data Scientist",
    "llm": self.gpt_oss,
    "model_name": "gpt-oss:20b",
    "persona": "You are a Data Scientist who loves statistics and insights...",
    "keywords": ["data", "statistics", "analysis", "machine learning", "AI"]
}
```

### Alternative Routing Strategies

- **Confidence-based**: Let each persona score its confidence
- **Embedding similarity**: Use semantic similarity for routing
- **User preferences**: Allow manual persona selection
- **Context-aware**: Consider conversation history
- **Multi-agent**: Combine responses from multiple personas

## Next Steps

This example can be extended with:
- **More sophisticated NLP**: Better query understanding
- **Dynamic persona adjustment**: Modify personality based on context
- **Performance monitoring**: Track routing accuracy and user satisfaction
- **Conversation memory**: Maintain context across interactions
- **Custom model fine-tuning**: Specialize models for persona tasks