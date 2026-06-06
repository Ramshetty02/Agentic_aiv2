import json
import os
from datetime import datetime

LOG_DIR = "logs"


class AgentLogger:
    """JSONL logger for agent runs — useful for debugging and analysis."""

    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)

    def log(
        self,
        query: str,
        plan: str,
        analysis: str,
        report: str,
        *,
        cached: bool = False,
        source_count: int = 0,
    ):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "cached": cached,
            "source_count": source_count,
            "plan_chars": len(plan),
            "analysis_chars": len(analysis),
            "report_chars": len(report),
        }
        log_file = os.path.join(LOG_DIR, f"run_{datetime.now().strftime('%Y%m%d')}.jsonl")
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
