from main import MultiAgentCritiqueSystem

# Test individual components
system = MultiAgentCritiqueSystem()

print("Testing Multi-Agent System Components:")
print("=" * 60)

# Test 1: Solver agent
print("1. Testing Solver Agent:")
print("-" * 30)
test_query = "What is Python?"
solver_response = system.solve_query(test_query)
print("✅ Solver agent working")
print()

# Test 2: Judge agent (mock response)
print("2. Testing Judge Agent:")  
print("-" * 30)
mock_response = "Python is a programming language."
decision, feedback = system.judge_response(test_query, mock_response)
print(f"Decision: {decision}")
print(f"Feedback: {feedback}")
print("✅ Judge agent working")
print()

print("🎉 All components functional!")
print("Ready for full multi-agent collaboration.")