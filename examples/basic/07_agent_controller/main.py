from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class AgentBasedController:
    def __init__(self):
        # Controller agent uses fast Gemma3:1b for routing decisions
        self.controller_llm = ChatOpenAI(
            model="gemma3:1b", 
            api_key="ollama", 
            base_url="http://localhost:11434/v1"
        )
        
        # Initialize specialist LLMs
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
        
        self.gemma3 = ChatOpenAI(
            model="gemma3:1b", 
            api_key="ollama", 
            base_url="http://localhost:11434/v1"
        )
        
        # Controller agent persona
        self.controller_persona = """You are an Intelligent Agent Controller responsible for routing queries to the most appropriate specialist agent.

Your role:
- Analyze incoming queries to understand their intent and requirements
- Consider the strengths and specialties of each available agent
- Make reasoned decisions about which agent is best suited for the task
- Provide clear explanations for your routing decisions

You must be precise and decisive in your agent selection."""

        # Define available specialist agents
        self.specialist_agents = {
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
                "specialties": [
                    "Programming and software development",
                    "Technical explanations and tutorials", 
                    "Debugging and troubleshooting",
                    "Algorithm design and data structures",
                    "Code review and best practices",
                    "System architecture and design patterns"
                ]
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
                "specialties": [
                    "Creative writing and storytelling",
                    "Poetry and artistic expression",
                    "Fiction and narrative development",
                    "Character development and dialogue",
                    "Literary analysis and critique",
                    "Imaginative and artistic content"
                ]
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
                "specialties": [
                    "Business strategy and planning",
                    "Market analysis and research",
                    "Financial planning and analysis",
                    "Process optimization and efficiency",
                    "Risk assessment and management",
                    "Professional consulting and advice"
                ]
            },
            
            "witty_comedian": {
                "name": "Witty Comedian",
                "llm": self.gemma3,
                "model_name": "gemma3:1b",
                "persona": """You are a Witty Comedian who makes everything entertaining and fun.

Your personality traits:
- Clever and humorous
- Uses wordplay and witty observations
- Makes topics entertaining while staying informative
- Light-hearted and playful tone
- Always tries to make people smile""",
                "specialties": [
                    "Humor and entertainment",
                    "Jokes and comedic content",
                    "Light-hearted explanations",
                    "Witty observations and commentary",
                    "Fun and engaging content",
                    "Amusing takes on serious topics"
                ]
            }
        }

    def select_agent(self, query):
        """
        Use the controller agent to intelligently select the best specialist
        """
        # Build agent descriptions for the controller
        agent_descriptions = []
        for agent_key, agent_info in self.specialist_agents.items():
            specialties_text = "\n".join([f"  - {specialty}" for specialty in agent_info["specialties"]])
            agent_descriptions.append(f"""**{agent_info['name']}** ({agent_info['model_name']}):
{specialties_text}""")
        
        agents_text = "\n\n".join(agent_descriptions)
        
        controller_prompt = f"""You must select the best agent to handle this query.

QUERY: {query}

AVAILABLE AGENTS:
{agents_text}

Analyze the query and select the most appropriate agent. Respond in this exact format:

SELECTED_AGENT: [agent_name]
REASONING: [1-2 sentences explaining why this agent is the best choice]

Agent names to choose from: Dr. Code, Creative Writer, Business Analyst, Witty Comedian"""

        messages = [
            SystemMessage(content=self.controller_persona),
            HumanMessage(content=controller_prompt)
        ]
        
        response = self.controller_llm.invoke(messages)
        
        # Parse the controller's decision
        decision_text = response.content
        selected_agent = None
        reasoning = "No reasoning provided"
        
        try:
            lines = decision_text.split('\n')
            for line in lines:
                line_stripped = line.strip()
                if line_stripped.startswith('SELECTED_AGENT:'):
                    agent_name = line_stripped.split(':', 1)[1].strip()
                    # Map agent names to keys
                    name_to_key = {
                        "Dr. Code": "dr_code", 
                        "Creative Writer": "creative_writer",
                        "Business Analyst": "business_analyst",
                        "Witty Comedian": "witty_comedian"
                    }
                    selected_agent = name_to_key.get(agent_name)
                elif line_stripped.startswith('REASONING:'):
                    reasoning = line_stripped.split(':', 1)[1].strip()
        except:
            # Fallback to dr_code if parsing fails
            selected_agent = "dr_code"
            reasoning = "Parsing failed, defaulting to Dr. Code"
        
        if selected_agent is None:
            selected_agent = "dr_code"
            reasoning = "No valid agent selected, defaulting to Dr. Code"
        
        return selected_agent, reasoning, decision_text

    def process_query(self, query):
        """
        Complete process: controller selects agent -> specialist processes query
        """
        print("🧠 AGENT-BASED CONTROLLER")
        print("=" * 70)
        print(f"Query: {query}")
        print("=" * 70)
        print()
        
        # Step 1: Controller selects the best agent
        print("🤖 CONTROLLER DECISION:")
        print("-" * 50)
        selected_agent_key, reasoning, full_decision = self.select_agent(query)
        selected_agent = self.specialist_agents[selected_agent_key]
        
        print(f"Selected Agent: {selected_agent['name']} ({selected_agent['model_name']})")
        print(f"Reasoning: {reasoning}")
        print()
        print("Full Controller Response:")
        print(full_decision)
        print()
        
        # Step 2: Route to selected specialist agent
        print(f"🎯 SPECIALIST RESPONSE ({selected_agent['name']}):")
        print("-" * 50)
        
        messages = [
            SystemMessage(content=selected_agent["persona"]),
            HumanMessage(content=query)
        ]
        
        response = selected_agent["llm"].invoke(messages)
        
        print(response.content)
        print("=" * 70)
        
        return response.content

# Test the agent-based controller
if __name__ == "__main__":
    controller = AgentBasedController()
    
    # Test queries for comparison with keyword-based approach
    test_queries = [
        "How do I implement a binary search algorithm in Python?",
        "Write a short story about a robot discovering emotions",
        "What's the best strategy for entering a competitive market?", 
        "Tell me a funny joke about programming",
        "Explain machine learning in simple terms",
        "Create a poem about the beauty of mathematics"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*10} TEST QUERY {i} {'='*10}")
        controller.process_query(query)
        if i < len(test_queries):
            print("\n" + "⏸️ " * 20 + "\n")