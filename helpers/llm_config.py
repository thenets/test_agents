import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env file if it exists
if os.path.exists('.env'):
    load_dotenv('.env')

def is_openrouter_configured():
    """Check if OpenRouter is properly configured"""
    return bool(os.getenv("OPENROUTER_API_KEY"))

def configure_llm():
    """Configure the LLM with OpenRouter or local Ollama settings"""
    # Check if OpenRouter configuration is available
    if is_openrouter_configured():
        return ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            model=os.getenv("MODEL_NAME", "openai/gpt-4.1-nano"),
            temperature=0.1  # Lower temperature for more consistent math
        )
    else:
        # Fallback to local Ollama
        return ChatOpenAI(
            model="mistral",
            api_key="ollama",
            base_url="http://localhost:11434/v1",
            temperature=0.1
        )