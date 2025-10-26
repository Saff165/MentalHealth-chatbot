import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import random
import calendar

DB_PATH = "database/chatbot.db"

# --- Motivation + Examples ---
QUOTES = [
    "Healing isn’t overnight. Small steps count 🌱",
    "You’re stronger than your cravings 💪",
    "Progress, not perfection 💚",
    "Each sober sunrise is a victory ☀️",
    "Be kind to yourself today 🌿",
    "Your effort matters more than you think 💫"
]

DAILY_TASKS = ["🧘 Meditation", "🚶 Exercise", "🥗 Healthy meal", "💧 Hydration", "😴 Sleep on time"]

EXAMPLES = {
    "🧘 Meditation": [
        "10-minute guided breathing (Headspace/YouTube)",
        "Box breathing 4-4-6 (inhale-hold-exhale)",
        "Mindful body scan for 5 minutes"
    ],
    "🚶 Exercise": [
        "30-minute brisk walk",
        "15-minute yoga/stretch flow",
        "Short home workout: 3× (10 squats, 10 pushups, 20s plank)"
    ],
    "🥗 Healthy meal": [
        "Oats + fruits / sprouts salad",
        "Brown rice + dal + veggies",
        "Grilled paneer/chicken + salad"
    ],
    "💧 Hydration": [
        "Aim for ~2 litres (4× 500ml bottles)",
        "1 glass right after waking up",
        "Carry a bottle and sip every hour"
    ],
    "😴 Sleep on time": [
        "No phone 30 mins before bed",
        "Sleep target: before 11:00 PM",
        "Dark, cool room; slow breathing"
    ],
}

# ---------- DB helpers ----------
def _conn():
    return sqlite3.connect(DB_PATH)

def _ensure_month(username:str):
    """Ensure one row per day for the current month exists for the user."""
    y, m = date.today().year, date.today().month
    days_in_month = calendar.monthrange(y, m)[1]
    conn = _conn()
    c = conn.cursor()
    for day in range(1, days_in_month + 1):
        d = date(y, m, day).strftime("%Y-%m-%d")
        c.execute("SELECT 1 FROM recovery_tracker WHERE username=? AND date=?", (username, d))
        if not c.fetchone():
            c.execute(
                "INSERT INTO recovery_tracker (username,date,completed,motivation) VALUES (?,?,0,'')",
                (username, d)
            )
    conn.commit(); conn.close()

def _mark_done(username:str, d:str):
    conn = _conn()
    c = conn.cursor()
    quote = random.choice(QUOTES)
    c.execute("UPDATE recovery_tracker SET completed=1, motivation=? WHERE username=? AND date=?",
              (quote, username, d))
    conn.commit(); conn.close()
    return quote

def _load_df(username:str) -> pd.DataFrame:
    conn = _conn()
    df = pd.read_sql_query(
        "SELECT date, completed, motivation FROM recovery_tracker WHERE username=? ORDER BY date ASC",
        conn, params=(username,)
    )
    conn.close()
    if df.empty: return df
    df["date"] = pd.to_datetime(df["date"])
    return df

def _streak_current_month(df: pd.DataFrame) -> int:
    if df.empty: return 0
    df = df.sort_values("date")
    today = pd.Timestamp(date.today())
    # only this month
    df = df[df["date"].dt.month == today.month]
    if df.empty: return 0
    streak = 0
    for _, row in df.iloc[::-1].iterrows():
        day = row["date"].date()
        if day == (today - pd.Timedelta(days=streak)).date() and int(row["completed"]) == 1:
            streak += 1
        else:
            break
    return streak

# ---------- UI ----------
def _examples_ui():
    with st.expander("📘 Daily Plan Examples (tap to view)", expanded=False):
        cols = st.columns(5)
        keys = list(EXAMPLES.keys())
        for i, k in enumerate(keys):
            with cols[i]:
                st.markdown(f"**{k}**")
                for tip in EXAMPLES[k]:
                    st.markdown(f"- {tip}")

def _calendar_grid(df_month: pd.DataFrame, username: str):
    """Draw a month grid with buttons (✅ done / ⚪ pending)."""
    today = date.today()
    first_weekday, days_in_month = calendar.monthrange(today.year, today.month)
    # Build a lookup for completion by day number
    done_days = {int(d.strftime("%d")) for d in df_month[df_month["completed"] == 1]["date"]}

    # 6 rows x 7 columns typical calendar
    rows = 6
    cols = st.columns(7)
    day_num = 1
    clicked_day = None

    for r in range(rows):
        for c in range(7):
            idx = r*7 + c
            if idx < first_weekday or day_num > days_in_month:
                cols[c].markdown("&nbsp;")
                continue
            # label
            emoji = "✅" if day_num in done_days else ("🔘" if day_num == today.day else "⚪")
            label = f"{emoji} {day_num}"
            key = f"cal_{today.year}_{today.month}_{day_num}"
            if cols[c].button(label, key=key):
                clicked_day = day_num
            day_num += 1

    # If a day clicked: show details / allow marking today
    if clicked_day:
        clicked_str = date(today.year, today.month, clicked_day).strftime("%Y-%m-%d")
        is_today = (clicked_day == today.day)
        status = "Completed" if clicked_day in done_days else "Pending"
        st.info(f"**{clicked_str}** – Status: **{status}**")
        if is_today and clicked_day not in done_days:
            if st.button("Mark **today** as done ✅", key="mark_from_grid"):
                q = _mark_done(username, clicked_str)
                st.success(f"Great job! {q}")
                st.rerun()
        elif not is_today:
            st.caption("You can only mark **today** from here. Past days are view-only.")

def show_calendar(username: str):
    _ensure_month(username)

    st.markdown(f"### 📆 Recovery – **{calendar.month_name[date.today().month]} {date.today().year}**")

    # ---- Checklist (kept as you requested) ----
    st.markdown("#### ✅ Today’s Checklist")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.checkbox("🧘 Meditation", key="task_med")
    c2.checkbox("🚶 Exercise", key="task_ex")
    c3.checkbox("🥗 Healthy meal", key="task_food")
    c4.checkbox("💧 Hydration", key="task_hyd")
    c5.checkbox("😴 Sleep on time", key="task_sleep")

    # Button to confirm today done
    if st.button("Mark today as done ✅", key="mark_today_btn"):
        today_str = date.today().strftime("%Y-%m-%d")
        q = _mark_done(username, today_str)
        st.success(f"Great job! {q}")
        st.rerun()

    # ---- Examples section (separate, not replacing checklist) ----
    _examples_ui()

    # ---- Load and show progress ----
    df = _load_df(username)
    if df.empty:
        st.info("No recovery data yet.")
        return

    today = date.today()
    df_month = df[df["date"].dt.month == today.month]
    done = int(df_month["completed"].sum())
    total = int(len(df_month))
    percent = (done/total*100) if total else 0.0
    streak = _streak_current_month(df)

    st.markdown(f"**This month:** {done}/{total} days completed (**{percent:.1f}%**). | 🔥 **Streak: {streak}** days")

    # ---- Calendar grid with buttons ----
    _calendar_grid(df_month, username)

    # ---- Bar chart (0/1 timeline) ----
    if not df_month.empty:
        fig, ax = plt.subplots()
        ax.bar(df_month["date"], df_month["completed"], width=0.8)
        ax.set_title("Daily Completion Tracker")
        ax.set_ylabel("1 = Completed, 0 = Missed")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig, clear_figure=True)

    # Gentle nudge if falling behind
    tail = df_month.tail(3)
    if len(tail) == 3 and tail["completed"].sum() == 0:
        st.warning("⚠️ You missed the last 3 days. It’s okay — restart today. I’m with you 💚")





