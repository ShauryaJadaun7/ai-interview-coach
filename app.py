import streamlit as st
import uuid
import json
from pathlib import Path
import time

from langgraph_agent import prep_graph, run_scoring
from logger import MetricAILogger
from utils.resume_parser import extract_text_from_pdf

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="AI Interview Coach | MetricAI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title(" AI Interview Coach")

# ====================== SESSION STATE ======================
if "execution_id" not in st.session_state:
    st.session_state.execution_id = str(uuid.uuid4())
    st.session_state.state = {
        "execution_id": st.session_state.execution_id,
        "resume_text": "",
        "job_description": "",
        "company_name": "",
        "role": "",
        "research_summary": "",
        "questions": [],
        "rationale": "",
        "interview_transcript": [],
        "scores": {},
        "improvement_plan": "",
        "final_report": ""
    }
    st.session_state.current_question_index = 0
    st.session_state.interview_active = False

logger = MetricAILogger()

# ====================== SIDEBAR - METRICAI DASHBOARD ======================
with st.sidebar:
    st.header(" Live Dashboard")
    st.markdown(f"**Execution ID:** `{st.session_state.execution_id[:8]}...`")
    
    log_path = Path("logs/runs.jsonl")
    if log_path.exists():
        logs = [json.loads(line) for line in log_path.read_text().splitlines()[-10:]]
        total_cost = sum(log.get("cost_inr", 0) for log in logs)
        st.metric("Total Cost (₹)", f"{total_cost:.2f}")
        st.metric("Steps Logged", len(logs))
    else:
        st.info("Logs will appear after first run")
    
  

# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs(["1. Upload & Prep", "2. Mock Interview", "3. Scoring & Report", "4. Raw Logs"])

# ====================== TAB 1: UPLOAD & PREP ======================
with tab1:
    st.subheader("Upload Resume + Job Details")
    
    uploaded_file = st.file_uploader("Resume (PDF)", type=["pdf"])
    if uploaded_file:
        with st.spinner("Extracting resume..."):
            st.session_state.state["resume_text"] = extract_text_from_pdf(uploaded_file)
            st.success("✅ Resume parsed successfully")
    
    st.session_state.state["company_name"] = st.text_input("Company Name", value="BlaiseLogic")
    st.session_state.state["role"] = st.text_input("Role", value="AI Engineer Intern")
    st.session_state.state["job_description"] = st.text_area("Job Description (paste full JD)", height=200)

    # === UPDATED BUTTON WITH CONFIG (this is what you asked for) ===
    if st.button("🚀 Generate Research + 10 Questions", type="primary"):
        if st.session_state.state["resume_text"] and st.session_state.state["job_description"]:
            with st.spinner("Running resilient prep phase (Research → Questions)..."):
                config = {"configurable": {"thread_id": st.session_state.execution_id}}
                result = prep_graph.invoke(st.session_state.state, config=config)
                
                st.session_state.state["research_summary"] = result.get("research_summary", "")
                st.session_state.state["questions"] = result.get("questions", [])
                st.session_state.state["rationale"] = result.get("rationale", "")
            
            st.success("✅ Research + Questions generated! Go to Tab 2.")
            st.rerun()
        else:
            st.error("Please upload resume and fill Job Description")

    # Show generated questions
    if st.session_state.state.get("questions"):
        st.subheader("Generated Interview Questions")
        for i, q in enumerate(st.session_state.state["questions"]):
            st.markdown(f"**Q{i+1}:** {q}")

# ====================== TAB 2: MOCK INTERVIEW ======================
with tab2:
    st.subheader("Live Mock Interview")
    if not st.session_state.state.get("questions"):
        st.info("Complete Tab 1 first")
    else:
        if st.button("Start Interview Now", type="primary") and not st.session_state.interview_active:
            st.session_state.interview_active = True
            st.rerun()

        if st.session_state.interview_active:
            # Show previous messages
            for msg in st.session_state.state["interview_transcript"]:
                if msg["role"] == "candidate":
                    st.chat_message("user").write(msg["content"])
                else:
                    st.chat_message("assistant").write(msg["content"])

            # Current question
            idx = st.session_state.current_question_index
            if idx < len(st.session_state.state["questions"]):
                q = st.session_state.state["questions"][idx]
                st.chat_message("assistant").write(f"**Question {idx+1}:** {q}")
                
                answer = st.chat_input("Type your answer here...")
                if answer:
                    st.session_state.state["interview_transcript"].append({"role": "candidate", "content": answer})
                    st.session_state.current_question_index += 1
                    st.rerun()

# ====================== TAB 3: SCORING ======================
with tab3:
    st.subheader("Scoring & Final Report")
    if st.button("Run Scoring (LLM-as-Judge)", type="primary"):
        if not st.session_state.state.get("interview_transcript"):
            st.error("Please complete the interview first")
        else:
            with st.spinner("Evaluating with strict rubric..."):
                scored = run_scoring(st.session_state.state)
                st.session_state.state.update(scored)
            st.success("✅ Scoring complete!")
            st.rerun()

    if st.session_state.state.get("final_report"):
        st.markdown("### 📋 Final Report")
        st.markdown(st.session_state.state["final_report"])
        
        st.markdown("### 💡 Improvement Plan")
        st.write(st.session_state.state["improvement_plan"])

# ====================== TAB 4: RAW LOGS ======================
with tab4:
    st.subheader("Raw MetricAI Logs")
    log_path = Path("logs/runs.jsonl")
    if log_path.exists():
        logs = [json.loads(line) for line in log_path.read_text().splitlines()]
        st.dataframe(logs, use_container_width=True)
        st.download_button("Download logs", log_path.read_text(), "metricai_logs.jsonl")
    else:
        st.info("No logs yet — run the agent first")

