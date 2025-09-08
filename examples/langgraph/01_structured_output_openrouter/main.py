import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from models import WeatherResponse, TaskAnalysisResponse, PersonResponse

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage | AIMessage]
    structured_response: WeatherResponse | TaskAnalysisResponse | PersonResponse | None

def configure_llm():
    """Configure the LLM with OpenRouter settings"""
    """return ChatOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("OPENROUTER_BASE_URL"),
        model=os.getenv("MODEL_NAME", "openai/gpt-oss-120b:free"),
        temperature=0.7,
    )"""
    return ChatOpenAI(
        model="mistral",
        api_key="ollama",
        base_url="http://localhost:11434/v1"
    )

def weather_agent_node(state: AgentState):
    """Node that processes weather queries with structured output"""
    llm = configure_llm()
    structured_llm = llm.with_structured_output(WeatherResponse)
    
    system_prompt = """You are a weather assistant. Given a weather query, provide accurate weather information 
    in the specified structured format. Use realistic weather data for the requested location."""
    
    messages = [HumanMessage(content=system_prompt)] + state["messages"]
    response = structured_llm.invoke(messages)
    
    return {
        "messages": state["messages"] + [AIMessage(content=f"Weather information retrieved for structured response")],
        "structured_response": response
    }

def task_analysis_agent_node(state: AgentState):
    """Node that processes task analysis queries with structured output"""
    llm = configure_llm()
    structured_llm = llm.with_structured_output(TaskAnalysisResponse)
    
    system_prompt = """You are a project management assistant. Given a project description, break it down 
    into specific tasks with priorities and time estimates. Provide practical recommendations."""
    
    messages = [HumanMessage(content=system_prompt)] + state["messages"]
    response = structured_llm.invoke(messages)
    
    return {
        "messages": state["messages"] + [AIMessage(content=f"Task analysis completed for structured response")],
        "structured_response": response
    }

def person_info_agent_node(state: AgentState):
    """Node that processes person information queries with structured output"""
    llm = configure_llm()
    structured_llm = llm.with_structured_output(PersonResponse)
    
    system_prompt = """You are an information assistant. Given a query about a person, provide 
    factual information in the specified structured format. Only include verified information."""
    
    messages = [HumanMessage(content=system_prompt)] + state["messages"]
    response = structured_llm.invoke(messages)
    
    return {
        "messages": state["messages"] + [AIMessage(content=f"Person information retrieved for structured response")],
        "structured_response": response
    }

def route_query(state: AgentState):
    """Determine which agent node to route to based on the query"""
    user_message = state["messages"][-1].content.lower()
    
    if any(keyword in user_message for keyword in ["weather", "temperature", "rain", "sunny", "cloudy"]):
        return "weather_agent"
    elif any(keyword in user_message for keyword in ["task", "project", "plan", "todo", "work"]):
        return "task_analysis_agent"
    elif any(keyword in user_message for keyword in ["who is", "person", "biography", "about"]):
        return "person_info_agent"
    else:
        return "weather_agent"

def create_structured_output_graph():
    """Create the LangGraph workflow for structured output processing"""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("weather_agent", weather_agent_node)
    workflow.add_node("task_analysis_agent", task_analysis_agent_node)
    workflow.add_node("person_info_agent", person_info_agent_node)
    
    workflow.set_conditional_entry_point(route_query)
    
    workflow.add_edge("weather_agent", END)
    workflow.add_edge("task_analysis_agent", END)
    workflow.add_edge("person_info_agent", END)
    
    return workflow.compile()

def print_structured_response(response):
    """Pretty print the structured response"""
    print("\n" + "="*50)
    print("STRUCTURED OUTPUT")
    print("="*50)
    
    if isinstance(response, WeatherResponse):
        print(f"Location: {response.location}")
        print(f"Condition: {response.condition.value}")
        print(f"Temperature: {response.temperature}°F")
        if response.humidity:
            print(f"Humidity: {response.humidity}%")
        print(f"Description: {response.description}")
        
    elif isinstance(response, TaskAnalysisResponse):
        print(f"Project: {response.project_name}")
        print(f"Total Tasks: {response.total_tasks}")
        print(f"Estimated Completion: {response.estimated_completion_time}")
        print("\nTasks:")
        for i, task in enumerate(response.tasks, 1):
            print(f"  {i}. {task.title} ({task.priority.value})")
            print(f"     {task.description}")
            if task.estimated_hours:
                print(f"     Estimated: {task.estimated_hours} hours")
        print("\nRecommendations:")
        for rec in response.recommendations:
            print(f"  • {rec}")
            
    elif isinstance(response, PersonResponse):
        print(f"Name: {response.name}")
        if response.age:
            print(f"Age: {response.age}")
        if response.occupation:
            print(f"Occupation: {response.occupation}")
        if response.location:
            print(f"Location: {response.location}")
        if response.notable_achievements:
            print("Notable Achievements:")
            for achievement in response.notable_achievements:
                print(f"  • {achievement}")
    
    print("="*50)

def main():
    """Main function to run the structured output example"""
    print("LangGraph + OpenRouter Structured Output Example")
    print("=" * 50)
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY not found in environment variables.")
        print("Please copy .env.example to .env and add your OpenRouter API key.")
        return
    
    graph = create_structured_output_graph()
    
    test_queries = [
        "What's the weather like in San Francisco today?",
        "I need to plan a website redesign project. Can you break it down into tasks?",
        "Who is Elon Musk and what are his main achievements?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 30)
        
        try:
            result = graph.invoke({
                "messages": [HumanMessage(content=query)],
                "structured_response": None
            })
            
            if result["structured_response"]:
                print_structured_response(result["structured_response"])
            else:
                print("No structured response generated.")
                
        except Exception as e:
            print(f"Error processing query: {e}")
    
    print("\nExample completed!")

if __name__ == "__main__":
    main()