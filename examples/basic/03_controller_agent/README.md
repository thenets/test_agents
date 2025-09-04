# Controller Agent - Dual LLM Router

This example demonstrates a controller agent that intelligently routes queries between two different LLMs based on the content and context of the query.

## What This Example Demonstrates

- **Multi-LLM orchestration**: Managing multiple language models within a single system
- **Intelligent routing**: Decision logic to select the most appropriate model for each query
- **Model specialization**: Leveraging different models' strengths for different types of tasks
- **Transparent selection**: Clear visibility into routing decisions and reasoning

## How It Works

The controller agent analyzes incoming queries and routes them to one of two Ollama models:

1. **GPT-OSS:20b**: Optimized for technical/coding queries
   - Triggered by keywords: code, programming, python, javascript, technical, debug, algorithm, function, class, variable

2. **Mistral**: Optimized for creative tasks
   - Triggered by keywords: creative, story, poem, write, narrative, fiction, artistic, literature, essay

### Routing Logic

The agent uses a simple keyword-based scoring system:
- Counts keyword matches for each model category
- Routes to the model with the highest score
- Defaults to GPT-OSS for neutral/tied queries
- Provides transparent reasoning for each routing decision

## Running the Example

1. Make sure Ollama is running locally on port 11434
2. Ensure both models are available:
   ```bash
   ollama pull gpt-oss:20b
   ollama pull mistral
   ```
3. Run the example:
   ```bash
   cd examples/basic/03_controller_agent
   python main.py
   ```

## Example Routing Scenarios

| Query | Expected Route | Reasoning |
|-------|---------------|-----------|
| "Write a creative story about a dragon" | Mistral | Creative writing keywords detected |
| "How do I implement binary search in Python?" | GPT-OSS:20b | Technical/programming keywords |
| "Explain artificial intelligence" | GPT-OSS:20b | Neutral query, default routing |
| "Create a poem about the ocean" | Mistral | Creative/artistic keywords |
| "Debug this JavaScript function" | GPT-OSS:20b | Technical/debugging keywords |

## Code Structure

- `ControllerAgent` class: Main controller with routing logic
- `route_query()`: Analyzes query and determines best model
- `process_query()`: Executes routing and returns response
- Test queries: Demonstrates different routing scenarios

## Customization Options

### Adding New Routing Rules

```python
# Add new keyword categories
self.data_analysis_keywords = ["analysis", "statistics", "data", "chart"]

# Modify routing logic
def route_query(self, query):
    # Add scoring for data analysis
    data_score = sum(1 for keyword in self.data_analysis_keywords if keyword in query_lower)
    # Update selection logic...
```

### Alternative Routing Strategies

- **Query length-based**: Route long queries to one model, short to another
- **Sentiment analysis**: Route based on query tone/sentiment  
- **User preferences**: Allow user to specify preferred model
- **Performance-based**: Route based on model response times
- **Confidence scoring**: Let models self-assess and route accordingly

## Next Steps

This example can be extended with:
- **More sophisticated NLP**: Use embeddings or classifiers for routing
- **Dynamic model loading**: Load models on-demand based on routing
- **Performance monitoring**: Track routing accuracy and model performance
- **Conversation context**: Consider conversation history in routing decisions
- **Model ensembling**: Combine responses from multiple models
- **Fallback strategies**: Handle cases where primary model is unavailable