from main import AgentBasedController

# Test with a clear humor query
controller = AgentBasedController()

test_query = "Make me laugh with a funny joke about cats"

print("Testing Humor Query:")
print("=" * 50)
print(f"Query: {test_query}")
print()

selected_agent_key, reasoning, full_decision = controller.select_agent(test_query)
selected_agent = controller.specialist_agents[selected_agent_key]

print("Controller Decision:")
print(f"Selected: {selected_agent['name']} ({selected_agent['model_name']})")
print(f"Reasoning: {reasoning}")