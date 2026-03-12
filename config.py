import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 100% FREE - Only Groq now
    MODEL_ORDER = ["llama-3.3-70b-versatile"]   # Best free model on Groq
    
    # API keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # Approx rates (for display only - free tier = ₹0)
    COST_RATES = {
        "llama-3.3-70b-versatile": {"input": 0.00059, "output": 0.00079}  # per 1K tokens
    }
    
    MAX_RETRIES = 3
    RETRY_DELAY = 2