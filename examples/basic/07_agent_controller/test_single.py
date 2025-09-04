from main import AgentBasedController

# Test with a single clear creative query
controller = AgentBasedController()

# Test a clearly creative query that should go to Creative Writer
test_query = "Write a magical story about a unicorn in an enchanted forest"

print("Testing Single Query:")
print("=" * 50)
print(f"Query: {test_query}")
print()

selected_agent_key, reasoning, full_decision = controller.select_agent(test_query)
selected_agent = controller.specialist_agents[selected_agent_key]

print("Controller Decision:")
print(f"Selected: {selected_agent['name']} ({selected_agent['model_name']})")
print(f"Reasoning: {reasoning}")
print()
print("Full Controller Response:")
print(full_decision)