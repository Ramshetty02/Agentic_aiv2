import streamlit as st
from agents.planner_agent import planner_agent
from agents.search_agent import search_agent
from agents.analyst_agent import analyst_agent
from agents.report_agent import report_agent
from agents.memory_agent import MemoryAgent
from utils.logger import AgentLogger

st.set_page_config(
    page_title="Agentic AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)

if "history" not in st.session_state:
    st.session_state.history = []
if "memory" not in st.session_state:
    st.session_state.memory = MemoryAgent()

logger = AgentLogger()
memory = st.session_state.memory

col1, col2 = st.columns([2, 1])
with col1:
    st.title("🤖 Agentic AI Research Assistant")
    st.caption("Pipeline: Plan → Search → Analyse → Report → Remember")
with col2:
    st.metric("Queries Researched", len(st.session_state.history))

user_query = st.text_area(
    "Enter your research task", height=80,
    placeholder="e.g. What are the latest AI agent frameworks in 2025?"
)

col_a, col_b, _ = st.columns([1, 1, 4])
with col_a:
    run = st.button("🚀 Run Agents", type="primary", use_container_width=True)
with col_b:
    clear = st.button("🗑️ Clear History", use_container_width=True)

if clear:
    st.session_state.history = []
    st.rerun()

if run and user_query.strip():
    similar = memory.get_similar(user_query)
    if similar:
        st.info(f"💡 Cached result for: *{similar['task']}*")
        with st.expander("View Cached Report"):
            st.markdown(similar["report"])

    progress = st.progress(0, text="Starting agents...")
    tabs = st.tabs(["📌 Plan", "🌐 Search", "📊 Analysis", "📝 Report"])

    with st.spinner("🧠 Planner Agent..."):
        plan = planner_agent(user_query)
        progress.progress(25, text="Plan ready...")
    with tabs[0]:
        st.markdown(plan)

    with st.spinner("🔍 Search Agent..."):
        search_results = search_agent(user_query)
        progress.progress(50, text="Data collected...")
    with tabs[1]:
        if isinstance(search_results, dict):
            st.json({k: v for k, v in search_results.items() if k != "raw_content"})
        else:
            st.write(search_results)

    with st.spinner("📊 Analyst Agent..."):
        analysis = analyst_agent(search_results)
        progress.progress(75, text="Analysis complete...")
    with tabs[2]:
        st.markdown(analysis)

    with st.spinner("📝 Generating report..."):
        report = report_agent(user_query, analysis)
        progress.progress(100, text="Done!")
    with tabs[3]:
        st.markdown(report)
        st.download_button(
            "⬇️ Download Report", report,
            file_name=f"report_{user_query[:30].replace(' ','_')}.md",
            mime="text/markdown"
        )

    memory.save(user_query, report)
    logger.log(user_query, plan, analysis, report)
    st.session_state.history.append({"query": user_query, "report": report})
    st.success("✅ Task Completed!")

with st.sidebar:
    st.header("📚 Research History")
    for i, item in enumerate(reversed(st.session_state.history[-10:])):
        idx = len(st.session_state.history) - i
        with st.expander(f"Q{idx}: {item['query'][:40]}..."):
            st.write(item["report"][:300] + "...")
