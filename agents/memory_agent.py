import sqlite3
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

DB_PATH = "database/memory.db"
THRESHOLD = 0.80

class MemoryAgent:
    """
    Semantic memory using SQLite + sentence-transformers.
    Finds similar past research sessions via cosine similarity — no heavy vector DB needed.
    """

    def __init__(self):
        os.makedirs("database", exist_ok=True)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    report TEXT NOT NULL,
                    embedding TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save(self, task: str, report: str):
        """Save a research session with its embedding."""
        embedding = self.model.encode(task).tolist()
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO memory (task, report, embedding) VALUES (?, ?, ?)",
                (task, report, json.dumps(embedding))
            )

    def get_similar(self, query: str, threshold: float = THRESHOLD):
        """Find semantically similar past research using cosine similarity."""
        q_emb = self.model.encode(query)
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "SELECT task, report, embedding FROM memory ORDER BY created_at DESC LIMIT 50"
            ).fetchall()

        best, best_score = None, 0.0
        for task, report, emb_str in rows:
            emb = np.array(json.loads(emb_str))
            score = float(
                np.dot(q_emb, emb) / (np.linalg.norm(q_emb) * np.linalg.norm(emb) + 1e-9)
            )
            if score > best_score:
                best_score, best = score, {"task": task, "report": report}

        return best if best_score >= threshold else None
