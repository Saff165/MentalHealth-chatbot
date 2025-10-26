import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "database/chatbot.db"

def _load(name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {name}", conn)
    conn.close()
    return df

def show_dashboard():
    st.markdown("### 👩‍⚕️ Therapist Dashboard")

    users = _load("users")
    logins = _load("login_activity")
    bookings = _load("therapist_booking")
    recovery = _load("recovery_tracker")
    progress = _load("progress")

    # Filters
    usernames = sorted(list(set(users["username"])) if not users.empty else [])
    selected = st.selectbox("Filter by user", ["All"] + usernames)

    def _maybe_filter(df):
        if df.empty: return df
        if selected == "All": return df
        if "username" in df.columns:
            return df[df["username"] == selected]
        return df

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Users")
        st.dataframe(users if selected == "All" else users[users["username"] == selected])
    with col2:
        st.subheader("Recent Logins")
        st.dataframe(_maybe_filter(logins).sort_values("id", ascending=False).head(100))

    st.subheader("Bookings")
    st.dataframe(_maybe_filter(bookings).sort_values("id", ascending=False).head(100))

    st.subheader("Recovery Tracker (recent)")
    st.dataframe(_maybe_filter(recovery).sort_values("date", ascending=False).head(120))

    st.subheader("Progress Logs (mood/craving/usage)")
    st.dataframe(_maybe_filter(progress).sort_values("date", ascending=False).head(120))

    # Exports
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        if not bookings.empty:
            st.download_button("⬇️ Download Bookings CSV", bookings.to_csv(index=False).encode("utf-8"),
                               file_name="bookings.csv", mime="text/csv")
    with exp_col2:
        if not recovery.empty:
            st.download_button("⬇️ Download Recovery CSV", recovery.to_csv(index=False).encode("utf-8"),
                               file_name="recovery.csv", mime="text/csv")

