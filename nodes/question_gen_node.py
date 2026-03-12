import time
from typing import Dict, Any
from model_router import ModelRouter
from logger import MetricAILogger
from config import Config
from prompts import InterviewQuestions, get_question_prompt
from utils.cost_calculator import calculate_cost

router = ModelRouter()
logger = MetricAILogger()

def question_gen_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node 2: Generate 10 tailored interview questions (structured output)"""
    start_time = time.time()
    model_name, model = router.get_model("gpt-4o-mini")
    
    structured_model = model.with_structured_output(InterviewQuestions)
    system_prompt, user_template = get_question_prompt()
    
    user_prompt = user_template.format(
        resume_text=state["resume_text"],
        job_description=state["job_description"],
        research_summary=state["research_summary"]
    )
    
    response = structured_model.invoke([("system", system_prompt), ("user", user_prompt)])
    
    tokens_in = response.usage_metadata.get("input_tokens", 0) if hasattr(response, "usage_metadata") else 0
    tokens_out = response.usage_metadata.get("output_tokens", 0) if hasattr(response, "usage_metadata") else 0
    latency = (time.time() - start_time) * 1000
    cost = calculate_cost(model_name, tokens_in, tokens_out)
    
    logger.log(
        execution_id=state["execution_id"],
        step="question_generation",
        model=model_name,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        latency_ms=latency,
        success=True,
        cost_inr=cost
    )
    
    return {
        "questions": response.questions,
        "rationale": getattr(response, "rationale", "")
    }