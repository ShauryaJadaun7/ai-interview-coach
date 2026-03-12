from config import Config

def calculate_cost(model_name: str, tokens_in: int, tokens_out: int) -> float:
    """
    Calculate approximate cost in INR.
    Used by logger and nodes for transparency.
    """
    if model_name not in Config.COST_RATES:
        return 0.0
    
    rates = Config.COST_RATES[model_name]
    cost_usd = (tokens_in * rates["input"] + tokens_out * rates["output"]) / 1000
    return round(cost_usd * 83, 4)  # 1 USD ≈ ₹83