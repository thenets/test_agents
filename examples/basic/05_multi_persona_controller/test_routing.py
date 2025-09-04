from main import MultiPersonaController

# Test just the routing logic without calling LLMs
controller = MultiPersonaController()

test_queries = [
    "How do I implement a binary search algorithm?",
    "Write a short story about a magical forest", 
    "What's the best strategy for entering a new market?",
    "Tell me a funny joke about programming",
    "Explain what artificial intelligence is",
    "Create a poem about the beauty of code"
]

print("Testing Multi-Persona Routing Logic:")
print("=" * 70)

for query in test_queries:
    agent_key, agent_info, reasoning = controller.route_query(query)
    print(f"Query: {query}")
    print(f"Selected: {agent_info['name']} ({agent_info['model_name']})")
    print(f"Reasoning: {reasoning}")
    print("-" * 50)