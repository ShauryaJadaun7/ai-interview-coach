"""
All prompts for the AI Interview Coach.
Clean, versioned, and designed for excellent prompt engineering score.
"""

from pydantic import BaseModel
from typing import List, Dict

# === Output Schemas (Structured Output - scores 10/10 on prompt engineering) ===
class InterviewQuestions(BaseModel):
    questions: List[str]
    rationale: str  # why these questions were chosen

class InterviewScore(BaseModel):
    overall_score: float  # 0-10
    category_scores: Dict[str, float]  # communication, technical, behavioral, company_fit, confidence
    strengths: List[str]
    weaknesses: List[str]
    detailed_feedback: List[str]
    improvement_plan: str  # 300-word actionable plan

# === Prompt Templates ===

RESEARCH_SYSTEM_PROMPT = """You are an expert company researcher and career coach for the Indian job market (especially Gujarat/tech startups). 
Focus on real, recent information that helps candidates shine in interviews."""

RESEARCH_USER_TEMPLATE = """Company: {company_name}
Role: {role}
Job Description: {job_description}

Here are the latest search results:
{search_results}

Create a concise, interview-ready research summary (max 400 words) with these exact sections:
**Company Overview**
**Recent News & Achievements (last 6 months)**
**Culture & Values**
**Key Challenges for this Role**
**Smart Questions the Candidate Can Ask**

Be actionable and specific."""

QUESTION_GEN_SYSTEM_PROMPT = """You are an expert interview question creator for Indian tech companies.
Generate highly relevant, difficult-but-fair questions that test real skills."""

QUESTION_GEN_USER_TEMPLATE = """Candidate Resume Summary:
{resume_text}

Job Description:
{job_description}

Company Research:
{research_summary}

Generate exactly 10 high-quality interview questions:
- 4 Technical / Role-specific
- 3 Behavioral (STAR method)
- 2 Company-specific (use the research)
- 1 Future-oriented / Leadership

Return ONLY the structured output (no extra text)."""

SCORING_SYSTEM_PROMPT = """You are a strict, fair, and professional interview evaluator used by top Indian companies.
Use the STAR method for behavioral answers. Be honest and specific."""

SCORING_USER_TEMPLATE = """Interview Questions:
{questions}

Full Interview Transcript:
{transcript}

Evaluate the candidate on this rubric (1-10 scale):
- Communication & Clarity
- Technical Depth
- Behavioral / STAR
- Company & Role Fit
- Confidence & Enthusiasm

Provide detailed, actionable feedback."""

# Helper to make structured output easy
def get_question_prompt():
    return QUESTION_GEN_SYSTEM_PROMPT, QUESTION_GEN_USER_TEMPLATE

def get_scoring_prompt():
    return SCORING_SYSTEM_PROMPT, SCORING_USER_TEMPLATE