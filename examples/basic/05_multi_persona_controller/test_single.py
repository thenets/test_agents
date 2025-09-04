from main import MultiPersonaController

# Test with a single query to verify full functionality
controller = MultiPersonaController()

# Test a creative query that should route to Creative Writer + Mistral
test_query = "Write a short story about a robot learning to code"

print("Testing Multi-Persona Controller Full Functionality:")
print("=" * 70)
controller.process_query(test_query)