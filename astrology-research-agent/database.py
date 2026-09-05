import sqlite3
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path(__file__).parent / "astrology_library.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            teacher TEXT,
            source_url TEXT,
            language TEXT,
            transcript TEXT NOT NULL,
            analysis TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

def save_note(title: str, teacher: str, source_url: str, language: str, transcript: str, analysis: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO notes(title, teacher, source_url, language, transcript, analysis)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, teacher, source_url, language, transcript, analysis),
        )
        conn.commit()
        return cur.lastrowid

def search_notes(query: str) -> List[Dict[str, Any]]:
    q = f"%{query}%"
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, title, teacher, source_url, language, analysis, created_at
            FROM notes
            WHERE title LIKE ?
               OR teacher LIKE ?
               OR transcript LIKE ?
               OR analysis LIKE ?
            ORDER BY created_at DESC
            LIMIT 50
            """,
            (q, q, q, q),
        ).fetchall()
    return [dict(r) for r in rows]

def list_notes() -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, title, teacher, source_url, language, analysis, created_at
            FROM notes
            ORDER BY created_at DESC
            LIMIT 100
            """
        ).fetchall()
    return [dict(r) for r in rows]
