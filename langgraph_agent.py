import uuid
import time
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from nodes.research_node import research_node
from nodes.question_gen_node import question_gen_node
from nodes.scoring_node import scoring_node

# ====================== STATE ======================
class AgentState(TypedDict):
    execution_id: str
    resume_text: str
    job_description: str
    company_name: str
    role: str
    research_summary: str
    questions: List[str]
    rationale: str
    interview_transcript: List[Dict]
    scores: Dict
    improvement_plan: str
    final_report: str

# ====================== GRAPH BUILDERS ======================
def build_prep_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("research", research_node)
    workflow.add_node("generate_questions", question_gen_node)
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "generate_questions")
    workflow.add_edge("generate_questions", END)
    return workflow.compile(checkpointer=MemorySaver())

def run_scoring(state: AgentState):
    """Scoring graph with config"""
    workflow = StateGraph(AgentState)
    workflow.add_node("score", scoring_node)
    workflow.add_edge(START, "score")
    workflow.add_edge("score", END)
    app = workflow.compile(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": state["execution_id"]}}
    return app.invoke(state, config=config)

prep_graph = build_prep_graph()

# Quick test
if __name__ == "__main__":
    test_state = {
        "execution_id": str(uuid.uuid4()),
        "resume_text": "Test resume for BlaiseLogic",
        "job_description": "AI Engineer Intern",
        "company_name": "BlaiseLogic",
        "role": "AI Intern",
        "research_summary": "",
        "questions": [],
        "rationale": "",
        "interview_transcript": [],
        "scores": {},
        "improvement_plan": "",
        "final_report": ""
    }
    config = {"configurable": {"thread_id": test_state["execution_id"]}}
    print("🚀 Testing...")
    result = prep_graph.invoke(test_state, config=config)
    print("✅ Success! Questions:", len(result.get("questions", [])))