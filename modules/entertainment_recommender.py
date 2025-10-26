import random

# ---------------------------------------------
# ENTERTAINMENT RECOMMENDER MODULE
# ---------------------------------------------

ENTERTAINMENT_DB = {
    "english": {
        "music": [
            ("Relaxing Rain Sounds 🌧️", "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO"),
            ("Calm Acoustic Vibes 🎸", "https://open.spotify.com/playlist/37i9dQZF1DX2UgsUIg75Vg"),
            ("Positive Energy 🎵", "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0")
        ],
        "movies": [
            ("The Pursuit of Happyness 🎬", "https://www.youtube.com/results?search_query=the+pursuit+of+happyness+full+movie"),
            ("Inside Out (Animated) 💜", "https://www.youtube.com/results?search_query=inside+out+full+movie"),
            ("Paddington 🧸", "https://www.youtube.com/results?search_query=paddington+movie+english+full")
        ],
        "games": [
            ("Calm Relaxing Game 🎮", "https://poki.com/en/g/relaxing-games"),
            ("Stress Buster Ball 🏐", "https://poki.com/en/g/ball-blast"),
            ("Zen Garden 🌱", "https://poki.com/en/g/zen")
        ],
        "relax": [
            ("Guided Meditation 🧘", "https://www.youtube.com/results?search_query=guided+meditation+10+minutes"),
            ("Ocean Sounds 🌊", "https://www.youtube.com/results?search_query=ocean+wave+sounds+for+sleep"),
            ("Soft Piano Nights 🎹", "https://open.spotify.com/playlist/37i9dQZF1DWVqfgj8NZEp1")
        ]
    },
    "tamil": {
        "music": [
            ("Peaceful Tamil Melodies 🎶", "https://www.youtube.com/results?search_query=peaceful+tamil+melodies"),
            ("Tamil Love Instrumentals 💞", "https://www.youtube.com/results?search_query=tamil+instrumental+music+bgm"),
            ("Soothing Ilayaraja Classics 🎧", "https://www.youtube.com/results?search_query=ilayaraja+melody+songs")
        ],
        "movies": [
            ("Velaiilla Pattadhari (VIP) 🎥", "https://www.youtube.com/results?search_query=vip+tamil+full+movie"),
            ("Nanban 💚", "https://www.youtube.com/results?search_query=nanban+full+movie"),
            ("Oh My Kadavule 💖", "https://www.youtube.com/results?search_query=oh+my+kadavule+full+movie")
        ],
        "games": [
            ("Stress Buster Game 🎯", "https://poki.com/en/g/stress-relief-games"),
            ("Brain Calm Puzzle 🧩", "https://poki.com/en/g/mind-games"),
            ("Relax Bubble Pop 🫧", "https://poki.com/en/g/bubble-games")
        ],
        "relax": [
            ("Calm Nature Tamil 🕊️", "https://www.youtube.com/results?search_query=tamil+relaxation+music"),
            ("Meditation Tamil 🧘‍♀️", "https://www.youtube.com/results?search_query=tamil+guided+meditation"),
            ("Rain Ambience Tamil 🌧️", "https://www.youtube.com/results?search_query=tamil+rain+sounds")
        ]
    }
}

# ---------------------------------------------
# Function 1: List content by category
# ---------------------------------------------

def list_by_category(lang: str, category: str):
    """
    Returns list of (title, link) tuples for the given language and category.
    """
    lang = lang.lower()
    if lang not in ENTERTAINMENT_DB:
        lang = "english"  # default fallback
    if category not in ENTERTAINMENT_DB[lang]:
        return []
    return ENTERTAINMENT_DB[lang][category]

# ---------------------------------------------
# Function 2: Smart Suggestion based on mood
# ---------------------------------------------

def suggest(lang: str, mood: str, username: str = "Friend"):
    """
    Returns a personalized suggestion message based on mood.
    """
    name = username.capitalize()
    mood = mood.lower()
    lang = lang.lower()
    if lang not in ENTERTAINMENT_DB:
        lang = "english"

    if mood in ["stressed", "anxious"]:
        rec = random.choice(ENTERTAINMENT_DB[lang]["relax"])
        return f"{name}, take a short break 🌿 Try this to calm your mind: [{rec[0]}]({rec[1]})"
    elif mood in ["bored", "tired"]:
        rec = random.choice(ENTERTAINMENT_DB[lang]["games"])
        return f"{name}, looks like you need some fun 🎮 Try this: [{rec[0]}]({rec[1]})"
    elif mood in ["happy", "better"]:
        rec = random.choice(ENTERTAINMENT_DB[lang]["music"])
        return f"Awesome, {name}! Keep that good energy with {rec[0]}: {rec[1]}"
    else:
        rec = random.choice(ENTERTAINMENT_DB[lang]["movies"])
        return f"{name}, here’s something inspiring to watch 🎥 {rec[0]}: {rec[1]}"
