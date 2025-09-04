from main import AgentBasedController

# Test the fixed routing with targeted queries designed to test each agent
controller = AgentBasedController()

# Targeted test queries - each should clearly route to a specific agent
test_cases = [
    {
        "query": "Tell me a funny joke about programming",
        "expected": "Witty Comedian",
        "description": "Clear humor request"
    },
    {
        "query": "What's the best market entry strategy for a tech startup?", 
        "expected": "Business Analyst",
        "description": "Business strategy question"
    },
    {
        "query": "How do I implement a binary search algorithm in Python?",
        "expected": "Dr. Code", 
        "description": "Technical programming question"
    },
    {
        "query": "Write a magical story about a unicorn in an enchanted forest",
        "expected": "Creative Writer",
        "description": "Creative writing request"
    },
    {
        "query": "Make me laugh with a cat joke",
        "expected": "Witty Comedian",
        "description": "Another humor request"
    },
    {
        "query": "Analyze the competitive landscape for our product launch",
        "expected": "Business Analyst", 
        "description": "Business analysis request"
    }
]

print("Testing Fixed Agent-Based Controller Routing:")
print("=" * 70)

results = []
for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test_case['description']}")
    print(f"Query: {test_case['query']}")
    print(f"Expected: {test_case['expected']}")
    print("-" * 50)
    
    selected_agent_key, reasoning, full_decision = controller.select_agent(test_case['query'])
    selected_agent = controller.specialist_agents[selected_agent_key]
    
    print(f"Selected: {selected_agent['name']} ({selected_agent['model_name']})")
    print(f"Reasoning: {reasoning}")
    
    # Check if selection matches expectation
    is_correct = selected_agent['name'] == test_case['expected']
    result_symbol = "✅" if is_correct else "❌"
    print(f"Result: {result_symbol} {'CORRECT' if is_correct else 'INCORRECT'}")
    
    results.append({
        'test': test_case['description'],
        'expected': test_case['expected'],
        'selected': selected_agent['name'],
        'correct': is_correct
    })

print("\n" + "=" * 70)
print("SUMMARY RESULTS:")
print("=" * 70)

correct_count = sum(1 for r in results if r['correct'])
total_count = len(results)

for result in results:
    symbol = "✅" if result['correct'] else "❌"
    print(f"{symbol} {result['test']}: Expected {result['expected']}, Got {result['selected']}")

print(f"\nOverall: {correct_count}/{total_count} correct ({correct_count/total_count*100:.1f}%)")

# Check if all agents were selected at least once
selected_agents = set(r['selected'] for r in results)
all_agents = {"Dr. Code", "Creative Writer", "Business Analyst", "Witty Comedian"}
agents_used = len(selected_agents)

print(f"Agent diversity: {agents_used}/4 agents used")
print(f"Agents selected: {', '.join(sorted(selected_agents))}")

if selected_agents == all_agents:
    print("🎉 All agents were selected - bias eliminated!")
else:
    unused = all_agents - selected_agents
    print(f"⚠️  Unused agents: {', '.join(unused)}")