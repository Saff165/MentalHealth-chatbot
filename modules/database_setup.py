import os
import sqlite3
from datetime import datetime

DB_PATH = "database/chatbot.db"

def init_database():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        language TEXT,
        joined_on TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS login_activity(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        login_time TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS progress(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        mood TEXT,
        craving INTEGER,
        usage INTEGER,
        risk TEXT,
        date TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS recovery_tracker(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        completed INTEGER DEFAULT 0,
        motivation TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS therapist_booking(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        time TEXT,
        mode TEXT,
        note TEXT,
        status TEXT DEFAULT 'Pending'
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS entertainment_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        emotion TEXT,
        type TEXT,
        content_link TEXT,
        date TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS awareness_clicks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        category TEXT,
        click_time TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS journal(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        entry TEXT,
        created_at TEXT
    )""")

    conn.commit()
    conn.close()

def upsert_user(username: str, language: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if row is None:
        c.execute("INSERT INTO users (username,language,joined_on) VALUES (?,?,?)",
                  (username, language, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    else:
        c.execute("UPDATE users SET language=? WHERE username=?", (language, username))
    conn.commit()
    conn.close()

def log_login(username: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO login_activity (username, login_time) VALUES (?,?)",
              (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


