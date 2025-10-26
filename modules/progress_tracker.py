import sqlite3
from datetime import datetime

DB_PATH = "database/chatbot.db"

def risk_label(mood:str|None, craving:int|None, usage:int|None) -> str:
    craving = craving or 0
    usage = usage or 0
    if usage >= 6 or craving >= 8:
        return "High"
    if usage >= 3 or craving >= 5:
        return "Medium"
    return "Low"

def log_progress(username, mood, craving, usage):
    risk = risk_label(mood, craving, usage)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO progress (username,mood,craving,usage,risk,date) VALUES (?,?,?,?,?,?)",
              (username, mood or "", craving or 0, usage or 0, risk, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return risk


