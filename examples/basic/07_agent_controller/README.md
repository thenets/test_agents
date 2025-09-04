# Agent-Based Controller System

This example demonstrates an intelligent controller that uses AI reasoning (rather than keyword matching) to select the most appropriate specialist agent for each query.

## What This Example Demonstrates

- **AI-Powered Routing**: LLM-based decision making for agent selection
- **Intelligent Analysis**: Understanding query intent and requirements
- **Reasoned Explanations**: Clear justification for routing decisions  
- **Mixed Model Strategy**: Optimal speed/quality balance across different models
- **Advanced Orchestration**: Smart delegation to specialist agents

## Key Difference from Example 5

| Aspect | Example 5 (Multi-Persona Controller) | Example 7 (Agent-Based Controller) |
|--------|--------------------------------------|-------------------------------------|
| **Routing Method** | Keyword-based scoring | AI reasoning and analysis |
| **Decision Logic** | Rule-based pattern matching | LLM-powered intent understanding |
| **Flexibility** | Fixed keyword associations | Adaptable to context and nuance |
| **Explanations** | Score-based reasoning | Natural language explanations |
| **Controller Model** | No LLM (just logic) | Gemma3:1b for fast reasoning |

## Architecture

### 🧠 Controller Agent (Gemma3:1b)
- **Role**: Intelligent routing decision maker
- **Capabilities**: 
  - Analyzes query intent and complexity
  - Considers specialist agent strengths
  - Makes reasoned selection decisions
  - Provides clear explanations

### 🎯 Specialist Agents

1. **Dr. Code (GPT-OSS:20b)**
   - **Specialties**: Programming, technical tutorials, debugging, algorithms
   - **Best for**: Complex technical content requiring depth

2. **Creative Writer (Mistral)** 
   - **Specialties**: Storytelling, poetry, fiction, artistic expression
   - **Best for**: Creative and imaginative content

3. **Business Analyst (GPT-OSS:20b)**
   - **Specialties**: Strategy, market analysis, professional consulting
   - **Best for**: Business and analytical content

4. **Witty Comedian (Gemma3:1b)**
   - **Specialties**: Humor, entertainment, light-hearted content
   - **Best for**: Quick, fun responses

## Process Flow

```
Query Input
    ↓
1. Controller Agent analyzes query + available specialists
    ↓
2. AI reasoning determines best agent match
    ↓ 
3. Controller provides selection + reasoning
    ↓
4. Query routed to selected specialist
    ↓
5. Specialist processes with appropriate persona
    ↓
Final Response
```

## Model Strategy

| Model | Role | Rationale |
|-------|------|-----------|
| **Gemma3:1b** | Controller + Comedian | Fast reasoning for routing and light content |
| **GPT-OSS:20b** | Technical + Business | Heavy lifting for complex analytical tasks |
| **Mistral** | Creative Writing | Specialized for artistic and creative content |

## Running the Example

1. Make sure Ollama is running locally on port 11434
2. Ensure all models are available:
   ```bash
   ollama pull gpt-oss:20b
   ollama pull mistral
   ollama pull gemma3:1b
   ```
3. Run the example:
   ```bash
   cd examples/basic/07_agent_controller
   python main.py
   ```

## Example Routing Scenarios

### Query: "How do I implement binary search in Python?"
- **Expected Selection**: Dr. Code
- **AI Reasoning**: "Technical programming question requiring detailed explanation and code examples"

### Query: "Write a story about a robot discovering emotions"
- **Expected Selection**: Creative Writer  
- **AI Reasoning**: "Creative writing request requiring narrative skills and emotional depth"

### Query: "What's the best market entry strategy?"
- **Expected Selection**: Business Analyst
- **AI Reasoning**: "Business strategy question requiring professional analysis and frameworks"

### Query: "Tell me a programming joke"
- **Expected Selection**: Witty Comedian
- **AI Reasoning**: "Humor request that can be handled quickly with entertaining content"

## Advantages of AI-Based Routing

### Contextual Understanding
- **Nuanced Analysis**: Understands subtle requirements beyond keywords
- **Intent Recognition**: Grasps the underlying purpose of queries
- **Complexity Assessment**: Evaluates difficulty and specialist needs

### Flexibility
- **Adaptive Decisions**: No rigid keyword rules to maintain
- **Context Sensitivity**: Same keywords can route differently based on context
- **Natural Extensions**: Easy to add new specialists without rule updates

### Transparency
- **Clear Explanations**: Natural language reasoning for decisions
- **Confidence Indicators**: Understanding of decision certainty
- **Debuggable Logic**: Can trace why specific selections were made

## Code Structure

- `AgentBasedController`: Main orchestrator class
- `controller_llm`: Gemma3:1b for fast routing decisions
- `specialist_agents`: Dictionary of 4 specialized agents with personas
- `select_agent()`: AI-powered agent selection with reasoning
- `process_query()`: End-to-end query processing with explanations

## Performance Benefits

### Speed Optimization
- **Fast Controller**: Gemma3:1b provides quick routing decisions
- **Targeted Processing**: Routes to optimal model for each task type
- **Efficient Resource Use**: Avoids heavy models for light tasks

### Quality Optimization  
- **Best Model Match**: Routes complex tasks to powerful models
- **Specialist Expertise**: Each agent optimized for their domain
- **Consistent Experience**: Appropriate persona for each interaction

## Comparison Testing

Run the same queries through both Example 5 (keyword-based) and Example 7 (AI-based) to compare:

### Routing Accuracy
- Edge cases where keywords might mislead
- Context-dependent decisions
- Multi-faceted queries requiring nuanced analysis

### Response Quality
- Appropriate specialist selection
- Persona consistency
- Overall user experience

## Next Steps

This example can be extended with:
- **Confidence Scoring**: Quantitative assessment of routing decisions
- **Multi-Agent Responses**: Consulting multiple specialists for complex queries
- **Learning from Feedback**: Improving routing decisions over time
- **Dynamic Specialist Pool**: Adding/removing agents based on query patterns
- **Performance Monitoring**: Tracking routing accuracy and user satisfaction