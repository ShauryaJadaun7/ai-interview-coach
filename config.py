import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    MODEL_ORDER = ["llama-3.3-70b-versatile"]   

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    

    COST_RATES = {
        "llama-3.3-70b-versatile": {"input": 0.00059, "output": 0.00079}  # per 1K tokens
    }
    
    MAX_RETRIES = 3
    RETRY_DELAY = 2