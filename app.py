import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

# --- Local modules ---
from modules.database_setup import init_database, upsert_user, log_login
from modules.keystroke_analyzer import KeystrokeAnalyzer
from modules.chatbot_logic import get_reply
from modules.recovery_calendar import show_calendar
from modules.therapist_booking import booking_form
from modules.therapist_dashboard import show_dashboard
from modules.awareness_icons import show_awareness
from modules.entertainment_recommender import list_by_category, suggest

# =========================
# INIT
# =========================
os.makedirs("assets", exist_ok=True)
init_database()
st.set_page_config(page_title="Recovery Companion", page_icon="🌿", layout="wide")

# =========================
# THEME + STYLES
# =========================
st.markdown("""
<style>
/* MAIN AREA */
.main {
    background-color: #F7FBFB;
    color: #102020;
    font-family: 'Lato', sans-serif;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #D1ECE9 0%, #F0FAF9 100%) !important;
}
section[data-testid="stSidebar"] * {
    color: #0B2726 !important;
    font-size: 15px;
}

/* HEADINGS */
h1, h2, h3, h4, h5, h6 {
    color: #073F3A !important;
    font-weight: 600;
}

/* BUTTONS */
.stButton>button {
    background-color: #47AFA3 !important;
    color: white !important;
    border-radius: 10px;
    font-weight: 600;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #67C3B9 !important;
    color: #082E2B !important;
}

/* CHAT BUBBLES */
.user-bubble {
    background: #C9EFE8;
    color: #083431;
}
.bot-bubble {
    background: #E5F7F3;
    color: #082F2C;
}
</style>
""", unsafe_allow_html=True)


# =========================
# SESSION DEFAULTS
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "language" not in st.session_state:
    st.session_state.language = "English"
if "is_therapist" not in st.session_state:
    st.session_state.is_therapist = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "keystroke" not in st.session_state:
    st.session_state.keystroke = KeystrokeAnalyzer()
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = True

# =========================
# CONDITIONAL SIDEBAR VISIBILITY
# =========================
if not st.session_state.logged_in:
    # Hide sidebar on login
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] {display: none;}
        div.block-container { max-width: 520px; margin: auto; padding-top: 9%; text-align: center; }
        </style>
    """, unsafe_allow_html=True)
else:
    # Show / hide after login using toggle state
    display_style = "block" if st.session_state.sidebar_visible else "none"
    st.markdown(f"""
        <style>
        section[data-testid="stSidebar"] {{ display: {display_style} !important; }}
        </style>
    """, unsafe_allow_html=True)

# =========================
# LOGIN PAGE (USER + THERAPIST)
# =========================
if not st.session_state.logged_in:
    # Logo (safe fallback)
    try:
        st.image("assets/logo.png", width=90)
    except Exception:
        st.markdown("<div style='font-size:64px;'>🌿</div>", unsafe_allow_html=True)

    st.title("🌿 Welcome to Recovery Companion")
    st.caption("Calm, caring support for addiction recovery — available 24×7.")

    username = st.text_input("Your name", key="login_name")
    language = st.selectbox("Preferred Language", ["English", "Tamil"], key="login_lang")

    # Therapist login
    with st.expander("🧑‍⚕️ Therapist Login"):
        t_id = st.text_input("Therapist ID", key="t_id")
        t_pw = st.text_input("Password", type="password", key="t_pw")
        if st.button("Login as Therapist", key="therapist_login_btn"):
            if t_id == "admin" and t_pw == "therapy123":
                st.session_state.logged_in = True
                st.session_state.is_therapist = True
                st.session_state.username = "Therapist"
                st.success("Welcome, Therapist 🧑‍⚕️")
                st.rerun()
            else:
                st.error("Invalid therapist credentials.")

    if st.button("Login", key="user_login_btn"):
        if username.strip():
            st.session_state.logged_in = True
            st.session_state.username = username.strip().capitalize()
            st.session_state.language = language
            upsert_user(st.session_state.username, language)
            log_login(st.session_state.username)
            st.success(f"Welcome, {st.session_state.username} 💚")
            st.rerun()
        else:
            st.warning("Please enter your name to continue.")
    st.stop()

# =========================
# SIDEBAR (AFTER LOGIN)
# =========================
try:
    st.sidebar.image("assets/logo.png", width=96)
except Exception:
    st.sidebar.write("🌿")

st.sidebar.markdown(f"### 👋 Welcome, {st.session_state.username}")
st.sidebar.caption("Your journey to healing begins here 🌱")

# Toggle sidebar button
if st.sidebar.button("🌿 Toggle Sidebar", key="toggle_sidebar_btn"):
    st.session_state.sidebar_visible = not st.session_state.sidebar_visible
    st.rerun()

# Navigation
if st.session_state.is_therapist:
    tab = st.sidebar.radio(
        "Navigate",
        ["📊 Therapist Dashboard", "🗂️ Patient Records"],
        key="therapist_nav"
    )
else:
    tab = st.sidebar.radio(
        "Navigate",
        ["💬 Chatbot", "📅 Recovery Tracker", "🎧 Entertainment", "⚠️ Awareness", "👩‍⚕️ Therapist Booking", "📊 Therapist Dashboard"],
        key="user_nav"
    )

# Logout
if st.sidebar.button("Logout", key="logout_btn"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# =========================
# USER MODE TABS
# =========================
if not st.session_state.is_therapist:

    # ---- CHATBOT ----
    if tab == "💬 Chatbot":
        st.header("💬 Recovery Chatbot")
        st.caption("Type anything you feel. I’ll respond with support, motivation, or helpful links.")
        st.markdown("---")

        # Use a form so the input clears automatically without session_state errors
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("Write here...", key="chat_input", placeholder="Type your message…")
            submitted = st.form_submit_button("Send 💬", use_container_width=True)

        if submitted and user_input.strip():
            try:
                reply = get_reply(user_input.strip(), st.session_state.username, st.session_state.language.lower())
            except Exception as e:
                reply = f"Sorry, something went wrong 💡 ({e})"

            ts = datetime.now().strftime("%I:%M %p")
            st.session_state.chat_history.append((f"You ({ts})", user_input.strip()))
            st.session_state.chat_history.append((f"Bot ({ts})", reply))
            st.rerun()

        # Clear Chat
        if st.button("🧹 Clear Chat", key="clear_chat_btn"):
            st.session_state.chat_history = []
            st.rerun()

        # Display chat (last 20)
        for sender, text in st.session_state.chat_history[-20:]:
            if sender.startswith("You"):
                st.markdown(f"<div class='user-bubble'><b>{sender}:</b> {text}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-bubble'><b>{sender}:</b> {text}</div>", unsafe_allow_html=True)

    # ---- RECOVERY TRACKER ----
    elif tab == "📅 Recovery Tracker":
        st.header("📅 Recovery Tracker")
        show_calendar(st.session_state.username)

    # ---- ENTERTAINMENT ----
    elif tab == "🎧 Entertainment":
        st.header("🎧 Entertainment Zone")
        st.caption("Explore soothing music, uplifting movies, fun games, and relaxation videos 🎶")

        lang = st.session_state.language.lower()
        mood = st.selectbox("How are you feeling now?", ["stressed", "bored", "happy", "lonely", "anxious", "tired"], key="mood_sel")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✨ Smart Suggestion", key="smart_suggest_btn"):
                st.info(suggest(lang, mood, st.session_state.username))

        with c2:
            if st.button("🎁 Show Multiple Picks", key="multi_picks_btn"):
                st.subheader("Here are some picks for you 🌈")
                results = []
                results += list_by_category(lang, "music")[:3]
                results += list_by_category(lang, "movies")[:3]
                results += list_by_category(lang, "relax")[:3]
                results += list_by_category(lang, "games")[:3]
                if results:
                    for title, link in results:
                        st.markdown(f"- [{title}]({link})")
                else:
                    st.info("No suggestions found yet. Try changing language.")

    # ---- AWARENESS ----
    elif tab == "⚠️ Awareness":
        st.header("⚠️ Addiction Awareness")
        show_awareness(st.session_state.username)

    # ---- BOOKING ----
    elif tab == "👩‍⚕️ Therapist Booking":
        st.header("👩‍⚕️ Book a Therapy Session")
        booking_form(st.session_state.username)

    # ---- USER VIEW OF DASHBOARD (if any quick metrics) ----
    elif tab == "📊 Therapist Dashboard":
        show_dashboard()

# =========================
# THERAPIST MODE
# =========================
if st.session_state.is_therapist:

    # ---- THERAPIST DASHBOARD ----
    if tab == "📊 Therapist Dashboard":
        st.header("📊 Therapist Overview")
        st.caption("Monitor overall patient engagement and progress trends.")

        try:
            conn = sqlite3.connect("database/chatbot.db")
            df = pd.read_sql("SELECT username, date FROM logins", conn)
            if df.empty:
                st.info("No login data available yet.")
            else:
                counts = df['username'].value_counts().reset_index()
                counts.columns = ["Username", "Login Count"]
                st.subheader("🧍 User Activity Count")
                st.dataframe(counts, use_container_width=True)

                plt.figure(figsize=(6, 4))
                plt.bar(counts["Username"], counts["Login Count"])
                plt.xlabel("User")
                plt.ylabel("Logins")
                plt.title("User Login Frequency")
                st.pyplot(plt)
        except Exception as e:
            st.error(f"Error loading dashboard data: {e}")
        finally:
            try:
                conn.close()
            except:
                pass

    # ---- PATIENT RECORDS ----
    elif tab == "🗂️ Patient Records":
        st.header("🗂️ Patient Recovery Records")
        st.caption("View patient recovery check-ins and recent activity.")
        try:
            conn = sqlite3.connect("database/chatbot.db")
            cur = conn.cursor()
            users = cur.execute("SELECT username, language FROM users").fetchall()
            if not users:
                st.info("No user data found.")
            else:
                for u, l in users:
                    st.markdown(f"### 🧍 {u} ({l})")
                    rows = cur.execute(
                        "SELECT date, completed FROM recovery_tracker WHERE username=? ORDER BY date DESC LIMIT 7",
                        (u,)
                    ).fetchall()
                    if rows:
                        for d, comp in rows:
                            st.markdown(f"- {d}: {'✅ Completed' if comp else '❌ Missed'}")
                    else:
                        st.write("No recovery tracker data yet.")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error fetching records: {e}")
        finally:
            try:
                conn.close()
            except:
                pass

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<footer>Disclaimer: This assistant provides educational support and is not a replacement for professional medical advice. "
    "If you’re in danger or considering self-harm, please seek immediate help.</footer>",
    unsafe_allow_html=True
)

