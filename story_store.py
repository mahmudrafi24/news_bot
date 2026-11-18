import os
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

DATA = Path(os.environ.get("TECH_NEWS_DATA_DIR", Path(__file__).resolve().parent / "data")).resolve()


def database():
    DATA.mkdir(mode=0o700, exist_ok=True)
    db = sqlite3.connect(DATA / "news.sqlite")
    db.row_factory = sqlite3.Row
    db.executescript("""
        CREATE TABLE IF NOT EXISTS stories (
            id TEXT PRIMARY KEY, original TEXT NOT NULL, source TEXT NOT NULL,
            url TEXT NOT NULL, reported TEXT NOT NULL, headline TEXT NOT NULL,
            summary TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'draft', published TEXT
        );
        CREATE TABLE IF NOT EXISTS runs (
            at TEXT NOT NULL, message TEXT NOT NULL
        );
    """)
    return db


def now():
    return datetime.now(timezone.utc)


