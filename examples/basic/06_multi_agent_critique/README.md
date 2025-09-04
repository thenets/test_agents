# Multi-Agent Critique System

This example demonstrates a collaborative multi-agent system where agents work together to improve response quality through critique and iteration.

## What This Example Demonstrates

- **Collaborative Problem Solving**: Multiple agents working together toward better solutions
- **Quality Control**: Automated review and critique of responses
- **Iterative Improvement**: Feedback loops for response refinement
- **Agent Specialization**: Different models for different roles (solver vs judge)

## System Architecture

### 🔧 Solver Agent (GPT-OSS:20b)
- **Role**: Primary problem solver
- **Persona**: Expert Problem Solver focused on comprehensive, accurate solutions
- **Capabilities**: 
  - Analyzes problems thoroughly
  - Provides step-by-step solutions
  - Incorporates feedback for improvement
  - Maintains context across iterations

### ⚖️ Judge Agent (Mistral)
- **Role**: Quality evaluator and critic
- **Persona**: Critical Judge who evaluates responses objectively
- **Evaluation Criteria**:
  - Accuracy: Is the information correct?
  - Completeness: Does it fully address the question?
  - Clarity: Is it well-explained and understandable?
  - Usefulness: Would this help solve the problem?

## Process Flow

```
Query Input
    ↓
1. Solver Agent attempts solution
    ↓
2. Judge Agent evaluates response
    ↓
3. Decision: PASS or FAIL?
    ↓
   PASS → Final approved response
    ↓
   FAIL → Feedback to Solver Agent
    ↓
4. Solver Agent incorporates feedback
    ↓
5. Repeat until PASS or max attempts reached
```

## Key Features

### Iterative Improvement
- **Feedback Integration**: Solver incorporates judge's critique
- **Context Preservation**: Each attempt builds on previous feedback
- **Maximum Attempts**: Prevents infinite loops (default: 3 attempts)

### Transparent Process
- **Step-by-Step Logging**: Clear visibility into each iteration
- **Decision Reasoning**: Judge explains pass/fail decisions
- **Attempt Tracking**: Numbered attempts for clarity

### Quality Assurance
- **Structured Evaluation**: Consistent criteria across evaluations
- **Specific Feedback**: Actionable suggestions for improvement
- **Binary Decisions**: Clear pass/fail determinations

## Running the Example

1. Make sure Ollama is running locally on port 11434
2. Ensure both models are available:
   ```bash
   ollama pull gpt-oss:20b
   ollama pull mistral
   ```
3. Run the example:
   ```bash
   cd examples/basic/06_multi_agent_critique
   python main.py
   ```

## Example Process

### Test Query
> "Explain how to implement a secure user authentication system for a web application"

### Typical Flow
1. **Attempt #1**: Solver provides initial response
2. **Judge Evaluation**: Reviews for completeness and security considerations
3. **Potential Feedback**: "Add details about password hashing and session management"
4. **Attempt #2**: Solver incorporates feedback, adds missing security details
5. **Judge Evaluation**: Approves improved response
6. **Result**: Final approved response with comprehensive security guidance

## Code Structure

- `MultiAgentCritiqueSystem`: Main orchestrator class
- `solve_query()`: Solver agent with feedback incorporation
- `judge_response()`: Judge agent with structured evaluation
- `process_query()`: Main iteration loop with attempt tracking
- Robust parsing of judge decisions and feedback

## Customization Options

### Modify Evaluation Criteria

```python
judge_persona = """Evaluate responses based on:
- Technical accuracy
- Code quality and best practices  
- Security considerations
- Performance implications
- Maintainability"""
```

### Adjust Iteration Parameters

```python
# Change maximum attempts
final_response = system.process_query(query, max_attempts=5)

# Add early stopping conditions
if confidence_score > 0.9:
    break
```

### Alternative Judge Formats

```python
# JSON-structured feedback
judge_prompt = """Respond in JSON format:
{
  "decision": "PASS/FAIL",
  "score": 1-10,
  "strengths": ["..."],
  "improvements": ["..."]
}"""
```

## Benefits of This Approach

### Quality Improvement
- **Higher Standards**: Multiple review rounds catch issues
- **Consistent Quality**: Structured evaluation criteria
- **Iterative Refinement**: Responses improve with feedback

### Model Specialization  
- **Solver Focus**: GPT-OSS optimized for technical problem-solving
- **Judge Perspective**: Mistral provides diverse evaluation viewpoint
- **Role Clarity**: Each agent has distinct responsibilities

### Scalability
- **Easy Extension**: Add more specialized judge agents
- **Flexible Criteria**: Modify evaluation standards per domain
- **Process Monitoring**: Full visibility into improvement cycles

## Real-World Applications

- **Content Quality Control**: Ensuring high-quality documentation
- **Code Review Automation**: Multi-pass code improvement
- **Educational Tutoring**: Iterative explanation refinement
- **Creative Writing**: Collaborative story development
- **Technical Consulting**: Thorough solution validation

## Next Steps

This example can be extended with:
- **Multiple Judge Agents**: Different specialists for different aspects
- **Confidence Scoring**: Quantitative quality metrics
- **Learning from Feedback**: Judge agents that improve over time
- **Domain-Specific Critics**: Specialized evaluation for different fields
- **Human-in-the-Loop**: Optional human validation steps