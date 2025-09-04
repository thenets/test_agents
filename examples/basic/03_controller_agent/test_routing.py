from main import ControllerAgent

# Test just the routing logic without actually calling the LLMs
controller = ControllerAgent()

test_queries = [
    "Write a creative story about a dragon",
    "How do I implement a binary search algorithm in Python?",
    "Explain the concept of artificial intelligence",
    "Create a poem about the ocean",
    "Debug this JavaScript function that isn't working",
    "Write a compelling essay about climate change"
]

print("Testing routing logic:")
print("=" * 60)

for query in test_queries:
    model_choice, reasoning = controller.route_query(query)
    print(f"Query: {query}")
    print(f"Model Selection: {model_choice}")
    print(f"Reasoning: {reasoning}")
    print("-" * 40)