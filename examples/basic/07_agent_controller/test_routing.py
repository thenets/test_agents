from main import AgentBasedController

# Test just the routing decision without full execution
controller = AgentBasedController()

test_queries = [
    "How do I implement binary search in Python?",
    "Write a short story about a robot",
    "What's the best market entry strategy?",
    "Tell me a programming joke",
    "Explain machine learning concepts",
    "Create a poem about technology"
]

print("Testing Agent-Based Controller Routing Decisions:")
print("=" * 70)

for i, query in enumerate(test_queries, 1):
    print(f"\nTest {i}: {query}")
    print("-" * 50)
    
    selected_agent_key, reasoning, full_decision = controller.select_agent(query)
    selected_agent = controller.specialist_agents[selected_agent_key]
    
    print(f"Selected: {selected_agent['name']} ({selected_agent['model_name']})")
    print(f"Reasoning: {reasoning}")
    print(f"Agent Key: {selected_agent_key}")
    
print("\n" + "=" * 70)
print("✅ Controller routing decisions complete!")
print("Run main.py to see full responses from selected agents.")