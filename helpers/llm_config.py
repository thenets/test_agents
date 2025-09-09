import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def configure_llm():
    """Configure the LLM with OpenRouter or local Ollama settings"""
    # Check if OpenRouter configuration is available
    """if os.getenv("OPENROUTER_API_KEY"):
        return ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL"),
            model=os.getenv("MODEL_NAME", "deepseek/deepseek-chat"),
            temperature=0.1  # Lower temperature for more consistent math
        )
    else:"""
        # Fallback to local Ollama
    return ChatOpenAI(
        model="mistral",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
        temperature=0.1
    )