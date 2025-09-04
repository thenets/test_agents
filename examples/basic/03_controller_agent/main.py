from langchain_openai import ChatOpenAI

class ControllerAgent:
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
        
        # Define routing keywords
        self.gpt_oss_keywords = [
            "code", "programming", "python", "javascript", "technical", 
            "debug", "algorithm", "function", "class", "variable"
        ]
        
        self.mistral_keywords = [
            "creative", "story", "poem", "write", "creative writing",
            "narrative", "fiction", "artistic", "literature", "essay"
        ]

    def route_query(self, query):
        """
        Determine which LLM to use based on query content.
        Returns tuple of (model_name, reasoning)
        """
        query_lower = query.lower()
        
        # Check for GPT-OSS keywords (technical/coding)
        gpt_score = sum(1 for keyword in self.gpt_oss_keywords if keyword in query_lower)
        
        # Check for Mistral keywords (creative)
        mistral_score = sum(1 for keyword in self.mistral_keywords if keyword in query_lower)
        
        if gpt_score > mistral_score:
            return "gpt-oss:20b", f"Technical query detected (score: {gpt_score} vs {mistral_score})"
        elif mistral_score > gpt_score:
            return "mistral", f"Creative query detected (score: {mistral_score} vs {gpt_score})"
        else:
            # Default to GPT-OSS for neutral queries
            return "gpt-oss:20b", f"Neutral query, using default model (scores tied: {gpt_score})"

    def process_query(self, query):
        """
        Route query to appropriate LLM and return response
        """
        model_choice, reasoning = self.route_query(query)
        
        print(f"Query: {query}")
        print(f"Model Selection: {model_choice}")
        print(f"Reasoning: {reasoning}")
        print("-" * 60)
        
        # Select the appropriate LLM
        if model_choice == "mistral":
            llm = self.mistral
        else:
            llm = self.gpt_oss
        
        # Get response
        response = llm.invoke(query)
        
        print(f"Response from {model_choice}:")
        print(response.content)
        print("=" * 60)
        
        return response.content

# Test the controller agent
if __name__ == "__main__":
    controller = ControllerAgent()
    
    # Test queries that should route to different models
    test_queries = [
        "Write a creative story about a dragon",
        "How do I implement a binary search algorithm in Python?",
        "Explain the concept of artificial intelligence",
        "Create a poem about the ocean",
        "Debug this JavaScript function that isn't working",
        "Write a compelling essay about climate change"
    ]
    
    for query in test_queries:
        controller.process_query(query)
        print("\n")