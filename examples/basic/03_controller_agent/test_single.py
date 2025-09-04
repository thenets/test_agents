from main import ControllerAgent

# Test with a single query to verify full functionality
controller = ControllerAgent()

# Test a creative query that should route to Mistral
test_query = "Write a short poem about coding"

print("Testing full controller agent functionality:")
print("=" * 60)
controller.process_query(test_query)