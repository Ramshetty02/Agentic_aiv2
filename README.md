# 🤖 Agentic AI Research Assistant v2.0

> A production-grade **multi-agent AI pipeline** that autonomously plans, searches, analyses, and reports on any research topic — with semantic memory across sessions.

## Architecture

```
User Query
    ↓
Planner Agent  (LangChain + Pydantic structured output)
    ↓
Search Agent   (DuckDuckGo + BeautifulSoup page scraper)
    ↓
Analyst Agent  (GPT-4o-mini chain-of-thought analysis)
    ↓
Report Agent   (Structured markdown report generation)
    ↓
Memory Agent   (SQLite + SentenceTransformer cosine similarity)
```

## Features

- **Structured Planning** — Pydantic-validated research plans via LangChain chains
- **Multi-Source Search** — DuckDuckGo + page scraping with BeautifulSoup
- **Deep Analysis** — Chain-of-thought prompting with GPT-4o-mini
- **Semantic Memory** — SentenceTransformer embeddings + cosine similarity search
- **Report Download** — Export reports as markdown files
- **Run History** — Sidebar with past research sessions
- **Agent Logger** — JSONL logs per run date

## Quick Start

```bash
git clone https://github.com/yourusername/agentic-ai-research-assistant
cd agentic-ai-research-assistant
pip install -r requirements.txt
cp .env.example .env  # Add OPENAI_API_KEY
streamlit run app.py
```

## Project Structure

```
├── app.py                     # Streamlit UI (wide layout, tabs, progress)
├── agents/
│   ├── planner_agent.py       # Pydantic structured plan
│   ├── search_agent.py        # Multi-source search
│   ├── analyst_agent.py       # LLM analysis chain
│   ├── report_agent.py        # Report generation
│   └── memory_agent.py        # Semantic memory (SQLite + BERT)
├── tools/
│   └── web_search.py          # DDG + page scraper
├── utils/
│   └── logger.py              # JSONL agent run logger
├── database/                  # Auto-created SQLite DB
└── logs/                      # Auto-created run logs
```

## Skills Demonstrated

| Skill | Where |
|-------|-------|
| Python + Type Hints | All agents |
| LangChain Chains + Prompt Templates | planner, analyst, report agents |
| Pydantic v2 Validation | planner_agent.py |
| Multi-Agent Orchestration | app.py |
| NLP Embeddings (Sentence-BERT) | memory_agent.py |
| SQLite Persistence | memory_agent.py |
| Web Scraping (BeautifulSoup) | search_agent.py, web_search.py |
| Streamlit UI (wide, tabs) | app.py |
| Error Handling + Logging | utils/logger.py, tools/ |
