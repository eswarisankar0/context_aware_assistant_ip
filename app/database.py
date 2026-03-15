"""
database.py — SQLite-backed persistent reminder storage.
Place this file inside app/ alongside action_router.py.
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Always resolves to project_root/data/reminders.db regardless of cwd
_HERE         = Path(__file__).resolve().parent   # → app/
_PROJECT_ROOT = _HERE.parent                      # → project root
DB_PATH       = _PROJECT_ROOT / "data" / "reminders.db"


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Create tables if they don't exist. Safe to call multiple times."""
    conn = _conn()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS reminders (
                id            TEXT PRIMARY KEY,
                message       TEXT NOT NULL,
                trigger_at    TEXT NOT NULL,
                status        TEXT NOT NULL DEFAULT 'pending',
                created_at    TEXT NOT NULL,
                fired_at      TEXT,
                cancelled_at  TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_status     ON reminders(status);
            CREATE INDEX IF NOT EXISTS idx_trigger_at ON reminders(trigger_at);
        """)
        conn.commit()
        logger.info("✅ SQLite DB ready at %s", DB_PATH)
    finally:
        conn.close()


# ── CRUD ───────────────────────────────────────────────────────────────────────

def save_reminder(reminder_id: str, message: str, trigger_at: datetime) -> None:
    conn = _conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO reminders (id, message, trigger_at, status, created_at) "
            "VALUES (?, ?, ?, 'pending', ?)",
            (reminder_id, message, trigger_at.isoformat(), datetime.utcnow().isoformat()),
        )
        conn.commit()
    finally:
        conn.close()


def mark_fired(reminder_id: str) -> None:
    conn = _conn()
    try:
        conn.execute(
            "UPDATE reminders SET status='fired', fired_at=? WHERE id=?",
            (datetime.utcnow().isoformat(), reminder_id),
        )
        conn.commit()
    finally:
        conn.close()


def mark_cancelled(reminder_id: str) -> bool:
    conn = _conn()
    try:
        cur = conn.execute(
            "UPDATE reminders SET status='cancelled', cancelled_at=? "
            "WHERE id=? AND status='pending'",
            (datetime.utcnow().isoformat(), reminder_id),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def get_all_reminders_db(status: Optional[str] = None) -> list[dict]:
    conn = _conn()
    try:
        if status:
            rows = conn.execute(
                "SELECT * FROM reminders WHERE status=? ORDER BY trigger_at DESC", (status,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM reminders ORDER BY trigger_at DESC"
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_pending_reminders_db() -> list[dict]:
    """Return pending reminders that haven't fired yet (trigger_at in future)."""
    conn = _conn()
    try:
        now = datetime.utcnow().isoformat()
        rows = conn.execute(
            "SELECT * FROM reminders WHERE status='pending' AND trigger_at > ? "
            "ORDER BY trigger_at",
            (now,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_reminder_by_id_db(reminder_id: str) -> Optional[dict]:
    conn = _conn()
    try:
        row = conn.execute(
            "SELECT * FROM reminders WHERE id=?", (reminder_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()