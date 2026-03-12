import time
from typing import Dict, Any
from model_router import ModelRouter
from logger import MetricAILogger
from config import Config
from prompts import InterviewScore, get_scoring_prompt
from utils.cost_calculator import calculate_cost

router = ModelRouter()
logger = MetricAILogger()

def scoring_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node 3: LLM-as-Judge scoring with structured output"""
    start_time = time.time()
    model_name, model = router.get_model("gpt-4o-mini")
    
    structured_model = model.with_structured_output(InterviewScore)
    system_prompt, user_template = get_scoring_prompt()
    
    transcript_str = "\n".join([f"{msg['role']}: {msg['content']}" 
                               for msg in state.get("interview_transcript", [])])
    
    user_prompt = user_template.format(
        questions="\n".join(state.get("questions", [])),
        transcript=transcript_str
    )
    
    response = structured_model.invoke([("system", system_prompt), ("user", user_prompt)])
    
    tokens_in = response.usage_metadata.get("input_tokens", 0) if hasattr(response, "usage_metadata") else 0
    tokens_out = response.usage_metadata.get("output_tokens", 0) if hasattr(response, "usage_metadata") else 0
    latency = (time.time() - start_time) * 1000
    cost = calculate_cost(model_name, tokens_in, tokens_out)
    
    logger.log(
        execution_id=state["execution_id"],
        step="scoring",
        model=model_name,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        latency_ms=latency,
        success=True,
        cost_inr=cost
    )
    
    return {
        "scores": response.category_scores,
        "improvement_plan": response.improvement_plan,
        "final_report": f"Overall Score: {response.overall_score}/10\n\n"
                        f"Strengths:\n" + "\n".join(response.strengths)
    }