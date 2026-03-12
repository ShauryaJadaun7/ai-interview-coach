import time
from typing import Dict, Any
from model_router import ModelRouter
from logger import MetricAILogger
from config import Config
from prompts import RESEARCH_SYSTEM_PROMPT, RESEARCH_USER_TEMPLATE
from tavily import TavilyClient
from utils.cost_calculator import calculate_cost

router = ModelRouter()
logger = MetricAILogger()
tavily = TavilyClient(api_key=Config.TAVILY_API_KEY)

def research_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node 1: Company research with web search"""
    start_time = time.time()
    model_name, model = router.get_model("gpt-4o-mini")
    
    search_results = tavily.search(
        query=f"{state['company_name']} recent news culture values {state['role']} Gujarat India",
        max_results=6
    )
    
    user_prompt = RESEARCH_USER_TEMPLATE.format(
        company_name=state["company_name"],
        role=state["role"],
        job_description=state["job_description"],
        search_results=str(search_results)
    )
    
    messages = [("system", RESEARCH_SYSTEM_PROMPT), ("user", user_prompt)]
    response = model.invoke(messages)
    
    tokens_in = response.usage_metadata.get("input_tokens", 0) if hasattr(response, "usage_metadata") else 0
    tokens_out = response.usage_metadata.get("output_tokens", 0) if hasattr(response, "usage_metadata") else 0
    latency = (time.time() - start_time) * 1000
    cost = calculate_cost(model_name, tokens_in, tokens_out)  # from utils
    
    logger.log(
        execution_id=state["execution_id"],
        step="research",
        model=model_name,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        latency_ms=latency,
        success=True,
        cost_inr=cost,
        metadata={"company": state["company_name"]}
    )
    
    return {"research_summary": response.content}