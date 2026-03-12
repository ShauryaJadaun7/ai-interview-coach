from langchain_groq import ChatGroq
from config import Config

class ModelRouter:
    def __init__(self):
        self.model = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=Config.GROQ_API_KEY
        )
    
    def get_model(self, preferred=None):
        """Simple retry loop (no extra package needed)"""
        for attempt in range(Config.MAX_RETRIES):
            try:
                # Quick test
                self.model.invoke("test")
                return "llama-3.3-70b-versatile", self.model
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed: {e}")
                if attempt == Config.MAX_RETRIES - 1:
                    raise
        return "llama-3.3-70b-versatile", self.model