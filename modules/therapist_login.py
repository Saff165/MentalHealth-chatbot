import streamlit as st
import sqlite3
from datetime import datetime

def therapist_portal():
    st.header("🔐 Therapist Login")
    st.caption("For authorized mental health professionals only.")

    # --- Login form ---
    therapist_user = st.text_input("Username")
    therapist_pass = st.text_input("Password", type="password")

    if st.button("Login as Therapist"):
        if therapist_user == "admin" and therapist_pass == "therapist123":
            st.session_state["therapist_logged_in"] = True
            st.success("Access granted ✅")
        else:
            st.error("Invalid credentials")

    # --- Once logged in ---
    if st.session_state.get("therapist_logged_in", False):
        st.subheader("🧠 Therapist Dashboard")
        st.caption("Patient insights and activity overview")

        # Connect to your DB
        conn = sqlite3.connect("recovery_data.db")
        c = conn.cursor()

        # Show patient data
        try:
            c.execute("SELECT username, last_login, language FROM users")
            users = c.fetchall()
        except:
            users = []

        if users:
            st.markdown("### 👩‍💼 Registered Users")
            for u in users:
                st.markdown(f"**Name:** {u[0]} | **Language:** {u[2]} | **Last Login:** {u[1]}")
        else:
            st.info("No users found in the database yet.")

        # Example: Show relapse/crisis logs if available
        try:
            c.execute("SELECT username, date, motivation FROM recovery_tracker WHERE completed=0")
            relapse_logs = c.fetchall()
            if relapse_logs:
                st.markdown("### ⚠️ Potential Risk Entries")
                for r in relapse_logs:
                    st.markdown(f"- {r[0]} missed activity on {r[1]} | Motivation: {r[2]}")
        except:
            pass

        # Logout for therapist
        if st.button("Logout Therapist"):
            st.session_state["therapist_logged_in"] = False
            st.experimental_rerun()
