from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class MultiAgentCritiqueSystem:
    def __init__(self):
        # Solver agent uses GPT-OSS for consistent reasoning
        self.solver_llm = ChatOpenAI(
            model="gpt-oss:20b", 
            api_key="ollama", 
            base_url="http://localhost:11434/v1"
        )
        
        # Judge agent uses Mistral for diverse perspective
        self.judge_llm = ChatOpenAI(
            model="mistral", 
            api_key="ollama", 
            base_url="http://localhost:11434/v1"
        )
        
        # Solver persona
        self.solver_persona = """You are an Expert Problem Solver tasked with providing comprehensive, accurate solutions.

Your approach:
- Analyze problems thoroughly
- Provide clear, step-by-step solutions
- Include examples when helpful
- Be precise and detailed
- If you receive feedback, carefully incorporate it to improve your response"""

        # Judge persona  
        self.judge_persona = """You are a Critical Judge who evaluates responses for quality and completeness.

Your evaluation criteria:
- Accuracy: Is the information correct?
- Completeness: Does it fully address the question?
- Clarity: Is it well-explained and easy to understand?
- Usefulness: Would this help someone solve the problem?

You must:
1. Make a PASS/FAIL decision
2. Provide specific, actionable feedback if FAIL
3. Be constructive but thorough in your critique"""

    def solve_query(self, query, feedback=None, attempt_number=1):
        """
        Solver agent attempts to answer the query, incorporating feedback if provided
        """
        print(f"🔧 SOLVER ATTEMPT #{attempt_number}")
        print("-" * 50)
        
        # Build the solver prompt
        if feedback:
            solver_prompt = f"""Original Query: {query}

PREVIOUS FEEDBACK FROM JUDGE:
{feedback}

Please provide an improved response that addresses the feedback above."""
        else:
            solver_prompt = query
        
        messages = [
            SystemMessage(content=self.solver_persona),
            HumanMessage(content=solver_prompt)
        ]
        
        response = self.solver_llm.invoke(messages)
        
        print(f"Solver Response:")
        print(response.content)
        print()
        
        return response.content

    def judge_response(self, query, response, attempt_number=1):
        """
        Judge agent evaluates the solver's response
        """
        print(f"⚖️  JUDGE EVALUATION #{attempt_number}")
        print("-" * 50)
        
        judge_prompt = f"""Original Query: {query}

Response to Evaluate:
{response}

Evaluate this response based on accuracy, completeness, clarity, and usefulness.

You must respond in this exact format:
DECISION: [PASS or FAIL]
REASONING: [Explain your decision]
FEEDBACK: [If FAIL, provide specific actionable feedback for improvement. If PASS, write "None needed."]"""

        messages = [
            SystemMessage(content=self.judge_persona),
            HumanMessage(content=judge_prompt)
        ]
        
        judge_response = self.judge_llm.invoke(messages)
        
        print("Judge Evaluation:")
        print(judge_response.content)
        print()
        
        # Parse the judge's response
        evaluation = judge_response.content
        decision = "FAIL"  # Default to fail if parsing fails
        feedback = None
        
        try:
            lines = evaluation.split('\n')
            for line in lines:
                if line.startswith('DECISION:'):
                    decision = line.split(':', 1)[1].strip().upper()
                elif line.startswith('FEEDBACK:'):
                    feedback = line.split(':', 1)[1].strip()
                    if feedback.lower() in ["none needed.", "none needed"]:
                        feedback = None
        except:
            # If parsing fails, extract manually or default
            if "PASS" in evaluation.upper():
                decision = "PASS"
            feedback = evaluation if decision == "FAIL" else None
        
        return decision, feedback

    def process_query(self, query, max_attempts=3):
        """
        Main process: solver attempts -> judge evaluates -> iterate if needed
        """
        print("🚀 MULTI-AGENT CRITIQUE SYSTEM")
        print("=" * 70)
        print(f"Query: {query}")
        print("=" * 70)
        print()
        
        feedback = None
        
        for attempt in range(1, max_attempts + 1):
            # Solver attempts to answer
            response = self.solve_query(query, feedback, attempt)
            
            # Judge evaluates the response
            decision, feedback = self.judge_response(query, response, attempt)
            
            if decision == "PASS":
                print("✅ FINAL RESULT: APPROVED")
                print("=" * 70)
                print("Approved Response:")
                print(response)
                return response
            elif attempt == max_attempts:
                print(f"❌ FINAL RESULT: MAX ATTEMPTS REACHED ({max_attempts})")
                print("=" * 70)
                print("Final Response (not approved):")
                print(response)
                return response
            else:
                print(f"🔄 ITERATION: Proceeding to attempt #{attempt + 1}")
                print()
        
        return response

# Test the multi-agent critique system
if __name__ == "__main__":
    system = MultiAgentCritiqueSystem()
    
    # Test query that might need iteration
    test_query = "Explain how to implement a secure user authentication system for a web application"
    
    # Process the query through the multi-agent system
    final_response = system.process_query(test_query, max_attempts=3)