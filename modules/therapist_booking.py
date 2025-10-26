import streamlit as st
import sqlite3

DB_PATH = "database/chatbot.db"

def booking_form(username: str):
    st.markdown("#### Book a Session")
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        date = col1.date_input("Preferred Date")
        time = col2.time_input("Preferred Time")
        mode = st.selectbox("Mode", ["Online", "In-person"])
        note = st.text_area("Short note (optional)")
        submitted = st.form_submit_button("Submit Booking")
    if submitted:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO therapist_booking (username,date,time,mode,note) VALUES (?,?,?,?,?)",
                  (username, str(date), str(time), mode, note))
        conn.commit()
        conn.close()
        st.success("Your session request has been submitted. A therapist will contact you. 💚")
