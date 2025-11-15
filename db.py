import sqlite3
from datetime import datetime

DB_NAME = "bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            stamps INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qr_codes (
            qr_id TEXT PRIMARY KEY,
            user_id INTEGER,
            is_used BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_stamps(user_id: int) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT stamps FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def add_stamp(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET stamps = stamps + 1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def reset_stamps(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET stamps = 0 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def create_qr(qr_id: str, user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO qr_codes (qr_id, user_id) VALUES (?, ?)", (qr_id, user_id))
    conn.commit()
    conn.close()

def use_qr(qr_id: str) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, is_used FROM qr_codes WHERE qr_id=?", (qr_id,))
    row = cursor.fetchone()
    if not row or row[1]:
        conn.close()
        return None
    user_id = row[0]
    cursor.execute("UPDATE qr_codes SET is_used=1 WHERE qr_id=?", (qr_id,))
    conn.commit()
    conn.close()
    return user_id
