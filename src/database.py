"""Thin data-access layer.

All helpers use parameterized queries. User-supplied values are passed as bound
parameters (``?`` placeholders) and are never interpolated into the SQL string.
This is the single approved way to reach the database in this service.
"""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager

from .config import get_settings


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    settings = get_settings()
    conn = sqlite3.connect(settings.database_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def fetch_all(query: str, params: tuple = ()) -> list[dict]:
    """Run a read query and return every row as a dict. Values are bound, not interpolated."""
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def fetch_one(query: str, params: tuple = ()) -> dict | None:
    """Run a read query and return the first row as a dict, or None."""
    with get_connection() as conn:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None


def execute(query: str, params: tuple = ()) -> int:
    """Run a write query and return the number of affected rows."""
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        return cursor.rowcount
