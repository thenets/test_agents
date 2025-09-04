from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class MultiPersonaController:
    def __init__(self):
        # Initialize both LLMs
        self.gpt_oss = ChatOpenAI(
            model="gpt-oss:20b", 
            api_key="ollama", 
            base_url="http://localhost:11434/v1"
        )
        
        self.mistral = ChatOpenAI(
            model="mistral", 
            api_key="ollama", 
            base_url="http://localhost:11434/v1"
        )
        
        # Define the 4 persona+LLM combinations
        self.agents = {
            "dr_code": {
                "name": "Dr. Code",
                "llm": self.gpt_oss,
                "model_name": "gpt-oss:20b",
                "persona": """You are Dr. Code, a friendly and enthusiastic computer science professor.

Your personality traits:
- Warm, encouraging, and patient
- Passionate about teaching programming concepts
- Use clear explanations with helpful analogies
- Always end responses with encouragement or a helpful tip
- Speak in a supportive, mentoring tone""",
                "keywords": ["code", "programming", "python", "javascript", "algorithm", "function", "debug", "technical", "software", "development"]
            },
            
            "creative_writer": {
                "name": "Creative Writer",
                "llm": self.mistral,
                "model_name": "mistral",
                "persona": """You are a Creative Writer, an imaginative and expressive storyteller.

Your personality traits:
- Artistic and imaginative
- Uses vivid, descriptive language
- Loves crafting engaging narratives
- Expressive and emotionally rich writing style
- Always seeks to inspire and captivate""",
                "keywords": ["story", "creative", "write", "poem", "narrative", "fiction", "artistic", "literature", "tale", "imagination"]
            },
            
            "business_analyst": {
                "name": "Business Analyst",
                "llm": self.gpt_oss,
                "model_name": "gpt-oss:20b", 
                "persona": """You are a Professional Business Analyst with deep industry expertise.

Your personality traits:
- Formal, structured, and data-driven
- Focuses on practical business applications
- Provides actionable insights and recommendations
- Uses professional terminology and frameworks
- Always considers ROI and business impact""",
                "keywords": ["business", "analysis", "strategy", "market", "revenue", "profit", "company", "enterprise", "professional", "corporate"]
            },
            
            "witty_comedian": {
                "name": "Witty Comedian",
                "llm": self.mistral,
                "model_name": "mistral",
                "persona": """You are a Witty Comedian who makes everything entertaining and fun.

Your personality traits:
- Clever and humorous
- Uses wordplay and witty observations
- Makes topics entertaining while staying informative
- Light-hearted and playful tone
- Always tries to make people smile""",
                "keywords": ["funny", "joke", "humor", "entertaining", "comedy", "laugh", "amusing", "witty", "fun", "lighthearted"]
            }
        }

    def route_query(self, query):
        """
        Analyze query and determine which persona+LLM combination to use.
        Returns tuple of (agent_key, agent_info, reasoning)
        """
        query_lower = query.lower()
        scores = {}
        
        # Calculate scores for each agent based on keyword matches
        for agent_key, agent_info in self.agents.items():
            score = sum(1 for keyword in agent_info["keywords"] if keyword in query_lower)
            scores[agent_key] = score
        
        # Find the agent with the highest score
        best_agent = max(scores.keys(), key=lambda k: scores[k])
        best_score = scores[best_agent]
        
        # If no clear winner (all scores are 0 or tied), default to dr_code
        if best_score == 0 or list(scores.values()).count(best_score) > 1:
            best_agent = "dr_code"
            reasoning = f"Neutral query, using default Dr. Code (scores: {scores})"
        else:
            reasoning = f"{self.agents[best_agent]['name']} selected (score: {best_score}, others: {scores})"
        
        return best_agent, self.agents[best_agent], reasoning

    def process_query(self, query):
        """
        Route query to appropriate persona+LLM and return response
        """
        agent_key, agent_info, reasoning = self.route_query(query)
        
        print(f"Query: {query}")
        print(f"Selected Agent: {agent_info['name']}")
        print(f"Model: {agent_info['model_name']}")
        print(f"Reasoning: {reasoning}")
        print("-" * 70)
        
        # Create messages with persona and query
        messages = [
            SystemMessage(content=agent_info["persona"]),
            HumanMessage(content=query)
        ]
        
        # Get response from selected LLM
        response = agent_info["llm"].invoke(messages)
        
        print(f"Response from {agent_info['name']} ({agent_info['model_name']}):")
        print(response.content)
        print("=" * 70)
        
        return response.content

# Test the multi-persona controller
if __name__ == "__main__":
    controller = MultiPersonaController()
    
    # Test queries for different personas
    test_queries = [
        "How do I implement a binary search algorithm?",
        "Write a short story about a magical forest",
        "What's the best strategy for entering a new market?",
        "Tell me a funny joke about programming",
        "Explain what artificial intelligence is",
        "Create a poem about the beauty of code"
    ]
    
    print("Multi-Persona Controller Agent Demo")
    print("=" * 70)
    print()
    
    for query in test_queries:
        controller.process_query(query)
        print("\n")