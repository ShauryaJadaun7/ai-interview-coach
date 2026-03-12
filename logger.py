import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/runs.jsonl")

class MetricAILogger:
    def __init__(self):
        LOG_FILE.parent.mkdir(exist_ok=True)
    
    def log(self, execution_id: str, step: str, model: str, 
            tokens_in: int, tokens_out: int, latency_ms: float,
            success: bool, cost_inr: float = 0.0, metadata: dict = None):
        
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "execution_id": execution_id,
            "step": step,
            "model": model,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "latency_ms": round(latency_ms, 2),
            "success": success,
            "cost_inr": round(cost_inr, 4),
            "metadata": metadata or {}
        }
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        
        print(f"✅ [MetricAI Log] {step} | {model} | ₹{cost_inr:.4f}")