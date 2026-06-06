# Agentic AI Research Assistant v2

> A modular **research pipeline** with LangChain, structured planning (Pydantic), multi-source web search, and semantic session memory — exploring agentic AI patterns.

[![CI](https://github.com/Ramshetty02/Agentic_aiv2/actions/workflows/ci.yml/badge.svg)](https://github.com/Ramshetty02/Agentic_aiv2/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Live Demo

Deploy to [Streamlit Community Cloud](https://share.streamlit.io/) in one click:

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io/) → **New app**
3. Set **Main file path** to `app.py`
4. Add `OPENAI_API_KEY` under **Secrets**
5. Deploy

Or run locally ( **no API key required** — Demo Mode works out of the box):

```bash
git clone https://github.com/Ramshetty02/Agentic_aiv2.git
cd Agentic_aiv2
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## AI Backend Options

| Mode | Cost | Setup |
|------|------|-------|
| **Demo** (default) | Free | Leave `OPENAI_API_KEY` blank — uses templates + live web search |
| **OpenAI** | Paid | Set `OPENAI_API_KEY` in `.env` |
| **Ollama** | Free | Install [Ollama](https://ollama.com), run `ollama pull llama3.2`, set `OLLAMA_MODEL=llama3.2` in `.env` |

## Architecture

```
User Query
    ↓
Planner Agent   (LangChain + Pydantic structured output)
    ↓  plan steps & key questions feed downstream agents
Search Agent    (DuckDuckGo API + BeautifulSoup page scraper)
    ↓
Analyst Agent   (GPT-4o-mini, plan-aware analysis)
    ↓
Report Agent    (Structured markdown report)
    ↓
Memory Agent    (SQLite + SentenceTransformer cosine similarity)
```

## Features

- **Plan-driven research** — Search and analysis use the planner's key questions, not just the raw query
- **Semantic memory** — Similar past sessions are detected via embeddings; choose cached report or fresh research
- **Multi-source search** — DuckDuckGo results enriched with page scraping
- **Structured outputs** — Pydantic-validated research plans via LangChain
- **Report export** — Download results as markdown
- **Run history** — Sidebar with past sessions
- **JSONL logging** — Per-day agent run logs for debugging

## Project Structure

```
├── app.py                     # Streamlit UI (pipeline orchestration)
├── agents/
│   ├── plan_schema.py         # Pydantic models (testable without API key)
│   ├── planner_agent.py       # LangChain plan generation
│   ├── search_agent.py        # Plan-driven multi-source search
│   ├── analyst_agent.py       # Plan-aware LLM analysis
│   ├── report_agent.py        # Report generation
│   └── memory_agent.py        # Semantic memory (SQLite + embeddings)
├── tools/
│   └── web_search.py          # DuckDuckGo + page scraper
├── utils/
│   └── logger.py              # JSONL agent run logger
├── tests/                     # pytest suite
└── .github/workflows/ci.yml   # GitHub Actions CI
```

## Skills Demonstrated

| Skill | Where |
|-------|-------|
| Python + Type Hints | All agents |
| LangChain Chains + Prompt Templates | planner, analyst, report agents |
| Pydantic v2 Validation | `planner_agent.py` |
| Pipeline Orchestration | `app.py` |
| NLP Embeddings (Sentence-BERT) | `memory_agent.py` |
| SQLite Persistence | `memory_agent.py` |
| Web Scraping (BeautifulSoup) | `search_agent.py`, `web_search.py` |
| Streamlit UI | `app.py` |
| Testing (pytest) | `tests/` |
| CI/CD (GitHub Actions) | `.github/workflows/ci.yml` |

## Testing

```bash
pytest tests/ -v
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for GPT-4o-mini |

## Author

**Ramshetty02** — [GitHub](https://github.com/Ramshetty02)

## License

MIT — see [LICENSE](LICENSE).
