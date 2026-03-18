# AI Interview Coach

**Resilient Multi-Step AI Agent with LangGraph + MetricAI Observability**  


## Problem It Solves
Helps Indian freshers and early-career candidates  prepare for real job interviews by providing company-specific questions, live mock practice, and professional scoring.

---

##  Architecture


**LLM Router**: Groq (Llama-3.3-70B) 
**Core Framework**: LangGraph (StateGraph + MemorySaver)  
**Observability**: Full MetricAI-style logging (`runs.jsonl`)

---

##  Key Features

- Intelligent 2-model LLM router with automatic fallback
- Real-time company research using Tavily
- Structured output (Pydantic) for 100% reliable JSON
- Live multi-turn mock interview
- Strict LLM-as-Judge scoring + detailed improvement plan
- Complete MetricAI simulation with token, latency & cost tracking
- 100% free on Groq free tier

---

##  Screenshots

**1. Upload Resume & Generate Questions**  
![Upload & Prep](./screenshots/prep.png)

**2. Live Mock Interview**  
![Live Interview](./screenshots/interview.png)

**3. Scoring & Improvement Plan**  
![Scoring Report](./screenshots/scoring.png)

**4. MetricAI Live Dashboard & Logs**  
![MetricAI Logs](./screenshots/logs.png)

---

## Demo video 
![Video](./screenshots/0cf74566-2f0b-4ea4-b841-7f0a588c0fb3.mp4)


## Tech Stack

- **LangGraph** – Production-grade multi-step agent workflow
- **Streamlit** – Fast interactive UI
- **Groq + OpenAI + Anthropic** – Smart LLM router
- **Tavily** – Real-time web research
- **PyMuPDF + Pydantic** – Resume parsing & structured output

---

##  How to Run

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Add your free API keys in .env:

- **GROQ_API_KEY=gsk_...**
- **TAVILY_API_KEY=tvly-...**

## Run the app
streamlit run app.py

### Project Structure
ai-interview-coach/
|-- app.py
|-- langgraph_agent.py
|-- model_router.py
|-- config.py
|-- prompts.py
|-- logger.py
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- .env.example
|-- Arch.pdf
|-- screenshots/
|   |-- 1-prep.png
|   |-- 2-interview.png
|   |-- 3-scoring.png
|   `-- 4-logs.png
|-- nodes/
|   |-- __init__.py
|   |-- research_node.py
|   |-- question_gen_node.py
|   |-- interview_node.py
|   `-- scoring_node.py
|-- utils/
|   |-- __init__.py
|   |-- resume_parser.py
|   `-- cost_calculator.py
`-- logs/
