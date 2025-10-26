import streamlit as st
import random

# ---- Motivation + Knowledge ----
MOTIVATION_QUOTES = [
    "Small changes make a big difference 🌱",
    "You deserve peace and health 💚",
    "Each day without it makes you stronger 💪",
    "Recovery is not a race. It’s your journey 🌿",
    "You’re not alone in this 🌻"
]

AWARENESS_DATA = {
    "Alcohol": {
        "emoji": "🍺",
        "health": [
            "Liver damage, anxiety, depression.",
            "Sleep disruption and dehydration.",
            "Memory loss and low concentration."
        ],
        "cost_hint": 250,  # ₹ per day typical
        "tips": [
            "Replace drinks with flavored water/juice.",
            "Avoid triggers (parties, late nights) early on.",
            "Seek therapy or community support."
        ],
        "facts": [
            "1 month alcohol-free → better sleep + ~20% higher energy.",
            "Even ‘social drinking’ impacts memory and skin health."
        ],
    },
    "Cigarettes": {
        "emoji": "🚬",
        "health": [
            "Lung disease, mouth cancer, heart issues.",
            "Premature aging and bad breath.",
            "Reduced stamina and oxygen levels."
        ],
        "cost_hint": 200,
        "tips": [
            "Use nicotine-free mints/sunflower seeds.",
            "Drink water during craving windows.",
            "Make a ‘no-smoking zone’ at home."
        ],
        "facts": [
            "Lungs start healing within 20 minutes of quitting.",
            "Quitting a pack/day can save ~₹6,000 per month."
        ],
    },
    "Drugs": {
        "emoji": "💉",
        "health": [
            "Brain chemistry damage and depression.",
            "Paranoia, panic attacks, loss of control.",
            "Organ failure and cognitive decline."
        ],
        "cost_hint": 1000,
        "tips": [
            "Seek medical detox under supervision.",
            "Surround yourself with positive people.",
            "Exercise as a healthy dopamine source."
        ],
        "facts": [
            "After ~90 days sober, brain reward pathways start repairing.",
            "Support groups can reduce relapse risk significantly."
        ],
    },
    "Mobile Overuse": {
        "emoji": "📱",
        "health": [
            "Eye strain, neck pain, reduced focus.",
            "Anxiety and poor sleep cycles.",
            "Social disconnection and FOMO."
        ],
        "cost_hint": 1000,  # monthly data/time proxy
        "tips": [
            "Use Digital Wellbeing app limits.",
            "No phone 1 hour before bed.",
            "Do one screen-free activity daily."
        ],
        "facts": [
            "Excess screen time reduces REM sleep quality.",
            "A 24-hour phone break improves mood and focus."
        ],
    },
}

# ---- Persistent UI State Keys ----
SEL_KEY = "aware_selected"
FREQ_KEY = "aware_freq"
AMT_KEY = "aware_amount"
RES_KEY = "aware_result"

def _init_state():
    if SEL_KEY not in st.session_state:
        st.session_state[SEL_KEY] = None
    if FREQ_KEY not in st.session_state:
        st.session_state[FREQ_KEY] = "Daily"
    if AMT_KEY not in st.session_state:
        st.session_state[AMT_KEY] = 100
    if RES_KEY not in st.session_state:
        st.session_state[RES_KEY] = None

def _money_calculator(default_hint: int):
    st.markdown("### 💰 Cost Estimator")
    st.radio("How often do you spend?", ["Daily", "Weekly"], horizontal=True, key=FREQ_KEY)
    st.number_input("Average spend (₹):", min_value=10, max_value=10000,
                    value=int(default_hint), key=AMT_KEY, step=10)

    if st.button("Calculate Yearly Cost 💸", key="calc_cost_btn"):
        days = 365 if st.session_state[FREQ_KEY] == "Daily" else 52
        total = int(st.session_state[AMT_KEY]) * days
        st.session_state[RES_KEY] = total

    # persist and show result after rerun
    if st.session_state[RES_KEY] is not None:
        st.success(f"You’re spending approximately **₹{st.session_state[RES_KEY]:,}/year**.")
        st.caption("Imagine redirecting that into self-care, fitness, or travel 🌿")

def show_awareness(username: str = "User"):
    """Renders improved awareness section (no top header here; keep it in app.py)."""
    _init_state()

    st.caption("Tap a category to learn about risks, costs, and recovery tips.")
    cols = st.columns(4)
    categories = list(AWARENESS_DATA.keys())

    # category buttons → persist selection
    for i, c in enumerate(categories):
        with cols[i]:
            if st.button(f"{c} {AWARENESS_DATA[c]['emoji']}", key=f"aw_btn_{c}"):
                st.session_state[SEL_KEY] = c
                # reset cost result when switching category
                st.session_state[RES_KEY] = None
                st.session_state[AMT_KEY] = AWARENESS_DATA[c]["cost_hint"]

    selected = st.session_state[SEL_KEY]
    if not selected:
        st.info("👆 Choose an addiction above to explore details.")
        return

    data = AWARENESS_DATA[selected]
    st.markdown(f"### {data['emoji']} **{selected} Awareness**")
    st.info(random.choice(MOTIVATION_QUOTES))

    st.markdown("#### ⚕️ Health Risks")
    for point in data["health"]:
        st.markdown(f"- {point}")

    st.markdown("#### 🌿 Recovery Tips")
    for tip in data["tips"]:
        st.markdown(f"- {tip}")

    st.markdown("#### 💡 Did You Know?")
    for fact in data["facts"]:
        st.markdown(f"- {fact}")

    st.divider()
    _money_calculator(default_hint=data["cost_hint"])
    st.markdown("---")
    st.caption("Education is the first step to recovery 💚")



