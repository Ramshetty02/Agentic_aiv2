"""LLM backend selection: demo (free), OpenAI, or Ollama (free local)."""

import os

from dotenv import load_dotenv

load_dotenv()

_MODES = ("demo", "openai", "ollama")


def get_mode() -> str:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if key and key not in ("your_key_here", "sk-your-key-here"):
        return "openai"
    if os.getenv("OLLAMA_MODEL", "").strip():
        return "ollama"
    return "demo"


def is_demo_mode() -> bool:
    return get_mode() == "demo"


def get_llm():
    """Return a LangChain chat model for the configured backend."""
    mode = get_mode()
    if mode == "openai":
        from langchain_openai import ChatOpenAI
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return ChatOpenAI(model=model, temperature=0.3)
    if mode == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.3,
        )
    raise RuntimeError("Demo mode does not use an LLM — call demo helpers instead.")


def mode_label() -> str:
    labels = {
        "demo": "Demo Mode (free — no API key)",
        "openai": f"OpenAI ({os.getenv('OPENAI_MODEL', 'gpt-4o-mini')})",
        "ollama": f"Ollama ({os.getenv('OLLAMA_MODEL', 'llama3.2')})",
    }
    return labels[get_mode()]
