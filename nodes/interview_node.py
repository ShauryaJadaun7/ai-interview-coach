from typing import Dict, Any
from logger import MetricAILogger
from utils.cost_calculator import calculate_cost

logger = MetricAILogger()

def interview_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Placeholder node for future full-graph version.
    In current version, real-time interview is handled interactively in app.py (Streamlit chat).
    This node can be used later for automated interview simulation.
    """
    # For now, just log that interview happened
    logger.log(
        execution_id=state["execution_id"],
        step="interview",
        model="user_interactive",
        tokens_in=0,
        tokens_out=0,
        latency_ms=0,
        success=True,
        cost_inr=0.0,
        metadata={"questions_answered": len(state.get("interview_transcript", []))}
    )
    return state  # No change needed