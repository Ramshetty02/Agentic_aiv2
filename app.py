import streamlit as st

from agents.plan_schema import format_plan
from agents.planner_agent import planner_agent
from agents.search_agent import search_agent
from agents.analyst_agent import analyst_agent
from agents.report_agent import report_agent
from agents.llm_backend import get_mode, mode_label
from utils.logger import AgentLogger
from utils.ui import (
    inject_styles,
    render_greeting,
    render_mode_badge,
    render_quick_actions,
    render_pipeline_inline,
    render_user_query,
    render_search_results,
    render_cache_prompt,
    render_sidebar,
)

st.set_page_config(
    page_title="EREVNA",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

_DEFAULTS = {
    "history": [],
    "memory": None,
    "pending_query": None,
    "cached_match": None,
    "query_input": "",
    "last_result": None,
    "view_history_idx": None,
    "auto_run_query": None,
}
for key, val in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

inject_styles()
logger = AgentLogger()


def get_memory():
    if st.session_state.memory is None:
        from agents.memory_agent import MemoryAgent
        st.session_state.memory = MemoryAgent()
    return st.session_state.memory


def _slug(text: str) -> str:
    return text[:30].replace(" ", "_").replace("/", "-")


def run_pipeline(user_query: str, *, cached: bool = False) -> None:
    render_user_query(user_query)
    progress = st.progress(0, text="Thinking…")

    render_pipeline_inline("plan", [])
    with st.spinner(None):
        plan = planner_agent(user_query)
        plan_md = format_plan(plan)
        progress.progress(25, text="Searching the web…")

    render_pipeline_inline("search", ["plan"])
    with st.spinner(None):
        search_results = search_agent(user_query, plan)
        progress.progress(50, text="Analyzing…")

    render_pipeline_inline("analyze", ["plan", "search"])
    with st.spinner(None):
        analysis = analyst_agent(search_results, plan, task=user_query)
        progress.progress(75, text="Writing report…")

    render_pipeline_inline("report", ["plan", "search", "analyze"])
    with st.spinner(None):
        report = report_agent(user_query, analysis, plan)
        progress.progress(100, text="Done")

    render_pipeline_inline(None, ["plan", "search", "analyze", "report"])
    progress.empty()

    st.session_state.last_result = {
        "query": user_query,
        "plan_md": plan_md,
        "search_results": search_results,
        "analysis": analysis,
        "report": report,
        "cached": cached,
        "_query_shown": True,
    }
    st.session_state.view_history_idx = None

    get_memory().save(user_query, report)
    logger.log(
        user_query, plan_md, analysis, report,
        cached=cached,
        source_count=len(search_results.get("web_results", [])),
    )
    st.session_state.history.append({"query": user_query, "report": report})


def show_cached_report(user_query: str, cached: dict) -> None:
    render_user_query(user_query)
    st.session_state.last_result = {
        "query": user_query,
        "plan_md": "",
        "search_results": {},
        "analysis": "",
        "report": cached["report"],
        "cached": True,
        "_query_shown": True,
    }
    st.session_state.view_history_idx = None
    logger.log(user_query, "", "", cached["report"], cached=True)
    st.session_state.history.append({"query": user_query, "report": cached["report"]})


def render_results(result: dict) -> None:
    if not result.get("_query_shown"):
        render_user_query(result["query"])

    tabs = st.tabs(["Report", "Analysis", "Sources", "Plan"])
    with tabs[0]:
        st.markdown(result["report"])
        st.download_button(
            "Download report",
            result["report"],
            file_name=f"report_{_slug(result['query'])}.md",
            mime="text/markdown",
        )
    with tabs[1]:
        st.markdown(result["analysis"] if result.get("analysis") else "_No analysis data._")
    with tabs[2]:
        if result.get("search_results"):
            render_search_results(result["search_results"])
        else:
            st.caption("No sources for this session.")
    with tabs[3]:
        st.markdown(result["plan_md"] if result.get("plan_md") else "_Loaded from cache._")


def _submit_query(query: str) -> None:
    query = query.strip()
    if not query:
        return
    similar = get_memory().get_similar(query)
    if similar:
        st.session_state.pending_query = query
        st.session_state.cached_match = similar
    else:
        run_pipeline(query)


# ── Sidebar ────────────────────────────────────────────────────────────────
render_sidebar(st.session_state.history, mode_label())

# ── Main ───────────────────────────────────────────────────────────────────
has_results = bool(st.session_state.last_result) or st.session_state.view_history_idx is not None

render_mode_badge(get_mode(), mode_label())
render_greeting(has_results)

if not has_results and not st.session_state.pending_query:
    render_quick_actions()

# Chat input (bottom bar — ChatGPT style)
prompt = st.chat_input("Ask anything")

if prompt:
    _submit_query(prompt)

if st.session_state.auto_run_query:
    q = st.session_state.auto_run_query
    st.session_state.auto_run_query = None
    _submit_query(q)

# Cache choice
if st.session_state.pending_query and st.session_state.cached_match:
    cached = st.session_state.cached_match
    render_cache_prompt(cached["task"])
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Use cached", type="primary", use_container_width=True):
            show_cached_report(st.session_state.pending_query, cached)
            st.session_state.pending_query = None
            st.session_state.cached_match = None
            st.rerun()
    with c2:
        if st.button("Run fresh", use_container_width=True):
            query = st.session_state.pending_query
            st.session_state.pending_query = None
            st.session_state.cached_match = None
            run_pipeline(query)

# History view
if st.session_state.view_history_idx is not None:
    idx = st.session_state.view_history_idx
    if 0 <= idx < len(st.session_state.history):
        item = st.session_state.history[idx]
        st.session_state.last_result = {
            "query": item["query"],
            "plan_md": "",
            "search_results": {},
            "analysis": "",
            "report": item["report"],
            "cached": False,
            "_query_shown": False,
        }

# Results
if st.session_state.last_result:
    render_results(st.session_state.last_result)
