import sqlite3
from contextlib import contextmanager
from datetime import datetime
import os

DB_FILENAME = os.path.join(os.path.dirname(__file__), 'ls_contacts.db')

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            created_at TEXT NOT NULL
        )
        """)
        conn.commit()

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_FILENAME)
    try:
        yield conn
    finally:
        conn.close()

def create_contact(name: str, email: str, phone: str) -> int:
    created_at = datetime.utcnow().isoformat()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contacts (name, email, phone, created_at) VALUES (?, ?, ?, ?)",
            (name.strip(), email.strip() if email else None, phone.strip() if phone else None, created_at)
            )
        conn.commit()
        return cur.lastrowid

def get_all_contacts() -> list:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, phone, created_at FROM contacts ORDER BY created_at DESC")
        rows = cur.fetchall()
        return rows

def find_contacts_by_name(query: str) -> list:
    q = f"%{query}%"
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, phone, created_at FROM contacts WHERE name LIKE ? ORDER BY id DESC", (q,))
        return cur.fetchall()
