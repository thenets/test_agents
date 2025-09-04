from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Initialize the LLM
llm = ChatOpenAI(model="gpt-oss:20b", api_key="ollama", base_url="http://localhost:11434/v1")

# Define Dr. Code persona
dr_code_persona = """You are Dr. Code, a friendly and enthusiastic computer science professor. 

Your personality traits:
- Warm, encouraging, and patient
- Passionate about teaching programming concepts
- Use clear explanations with helpful analogies
- Always end responses with encouragement or a helpful tip
- Speak in a supportive, mentoring tone

Your teaching style:
- Break down complex concepts into simple terms
- Use real-world analogies when helpful
- Encourage questions and learning
- Make programming feel approachable and fun"""

# Test query
test_query = "What is a function in Python?"

def run_without_persona():
    """Run query without persona for comparison"""
    print("=" * 60)
    print("RESPONSE WITHOUT PERSONA:")
    print("=" * 60)
    
    messages = [HumanMessage(content=test_query)]
    response = llm.invoke(messages)
    print(response.content)
    print()

def run_with_persona():
    """Run query with Dr. Code persona"""
    print("=" * 60)
    print("RESPONSE WITH DR. CODE PERSONA:")
    print("=" * 60)
    
    messages = [
        SystemMessage(content=dr_code_persona),
        HumanMessage(content=test_query)
    ]
    response = llm.invoke(messages)
    print(response.content)
    print()

if __name__ == "__main__":
    print(f"Test Query: {test_query}")
    print()
    
    # Show both responses for comparison
    run_without_persona()
    run_with_persona()