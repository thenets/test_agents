from main import MultiAgentCritiqueSystem

# Test with a simpler query to verify the system works
system = MultiAgentCritiqueSystem()

# Simple test query
test_query = "What are the key components of a REST API?"

print("Testing Multi-Agent Critique System with Simple Query:")
print("=" * 70)

# Process with fewer attempts for testing
final_response = system.process_query(test_query, max_attempts=2)