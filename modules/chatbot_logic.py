import random
import re

# --------------------------------------------
# RECOVERY CHATBOT LOGIC — MULTI-CONTENT EDITION 🌿
# --------------------------------------------

def _a(url: str, text: str) -> str:
    """Safe HTML link"""
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'

# Predefined HTML links for content
LINK_SPOTIFY_CALM  = _a("https://open.spotify.com/playlist/37i9dQZF1DWU0ScTcjJBdj", "Relaxing Playlist 🎧")
LINK_SPOTIFY_HAPPY = _a("https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC", "Happy Vibes 🎵")
LINK_MOVIES_FEEL   = _a("https://www.youtube.com/results?search_query=feel+good+movies+english+tamil+full+movie", "Feel-Good Movies 🎬")
LINK_COMEDY        = _a("https://www.youtube.com/results?search_query=tamil+comedy+scenes+or+english+funny+videos", "Funny Clips 😄")
LINK_GAME_RELAX    = _a("https://poki.com/en/g/relaxing-games", "Stress Relief Game 🎮")
LINK_EXERCISE      = _a("https://www.youtube.com/results?search_query=5+minute+home+exercise+for+stress+relief", "5-Minute Stress Relief Exercise 🏋️‍♀️")
LINK_MINDFUL_VIDEO = _a("https://www.youtube.com/results?search_query=guided+meditation+for+anxiety+10+minutes", "Guided Meditation 🧘‍♀️")
LINK_BREATHING     = _a("https://www.youtube.com/watch?v=inpok4MKVLM", "4-7-8 Breathing Technique 🌬️")
LINK_THERAPY       = _a("#therapist-booking", "Book a Therapy Session 💚")

# Keyword categories
SUBSTANCE_WORDS = ["drink", "alcohol", "smoke", "cigarette", "weed", "drugs"]
NEGATIONS = ["not", "no", "dont", "don't", "never", "without", "won't", "cannot", "can't"]

def _has_any(msg, words): return any(w in msg for w in words)

def _is_negated(msg, keywords):
    for neg in NEGATIONS:
        for kw in keywords:
            if f"{neg} {kw}" in msg or f"{neg} to {kw}" in msg:
                return True
    return False


# --------------------------------------------------
# MAIN CHATBOT REPLY LOGIC
# --------------------------------------------------

def get_reply(user_msg, username="Friend", lang="english"):
    msg = user_msg.lower().strip()
    name = username.capitalize()

    # ✅ 1. Prevent misclassification: “not to die”
    if re.search(r"\bnot\b.*\b(die|suicide|kill myself)\b", msg):
        return f"💚 That’s wonderful, {name}. Choosing life shows courage 🌱 You’re growing stronger every day."

    # 🚨 2. Crisis / self-harm check
    if _has_any(msg, ["die", "suicide", "end my life", "kill myself"]):
        return (
            f"⚠️ {name}, I sense you’re in deep distress.<br>"
            "You are <b>not alone</b>. Please reach out for help:<br>"
            "📞 <b>Snehi Helpline (India): 9152987821</b><br>"
            "💬 Talk to someone you trust.<br>"
            "Your life matters, {name}. Let’s take a slow breath together 💚"
        )

    # 🍺 3. Relapse trigger (alcohol/smoking/drug)
    if _has_any(msg, SUBSTANCE_WORDS):
        if _is_negated(msg, SUBSTANCE_WORDS):
            return f"💚 Great job, {name}! Avoiding cravings takes strength 🌿 Try {LINK_SPOTIFY_HAPPY} for motivation."
        return (
            f"It’s okay, {name}. Relapse thoughts don’t mean failure — recovery is a journey 🌱<br>"
            f"Let’s do something helpful together — try a grounding activity:<br>"
            f"➡️ {LINK_BREATHING}<br>"
            f"➡️ {LINK_EXERCISE}<br>"
            f"➡️ or {LINK_MINDFUL_VIDEO}<br>"
            "Would you like me to guide a short 2-minute breathing now?"
        )

    # 🧘 4. Exercise request
    if _has_any(msg, ["exercise", "workout", "stretch", "yoga", "move body"]):
        return (
            f"Great idea, {name}! Movement helps balance your mind 🌿<br>"
            f"Try these quick workouts:<br>"
            f"➡️ {LINK_EXERCISE}<br>"
            f"➡️ {LINK_BREATHING}<br>"
            f"➡️ {LINK_MINDFUL_VIDEO}<br>"
            "Would you like me to suggest one daily reminder for movement?"
        )

    # 🎮 5. Games request
    if _has_any(msg, ["game", "games", "play", "bored game"]):
        return (
            f"Here you go, {name}! 🎮 Try one of these to relax:<br>"
            f"➡️ {LINK_GAME_RELAX}<br>"
            f"➡️ {_a('https://poki.com/en/g/fidget-spinner','Fidget Spinner Game 🌀')}<br>"
            f"➡️ {_a('https://poki.com/en/g/zen','Zen Garden 🌸')}<br>"
            "Fun is therapy too — pick one and enjoy 🌿"
        )

    # 🎵 6. Music request
    if _has_any(msg, ["music", "song", "playlist", "tune", "melody"]):
        return (
            f"🎵 Music heals, {name}. Try these:<br>"
            f"➡️ {LINK_SPOTIFY_CALM}<br>"
            f"➡️ {LINK_SPOTIFY_HAPPY}<br>"
            f"➡️ {_a('https://open.spotify.com/playlist/37i9dQZF1DWVqfgj8NZEp1','Peaceful Piano Nights 🎹')}<br>"
            "Would you like a playlist that matches your current mood?"
        )

    # 🎬 7. Movie / video requests
    if _has_any(msg, ["movie", "film", "watch", "video", "show"]):
        return (
            f"Here’s something uplifting, {name} 🎬<br>"
            f"➡️ {LINK_MOVIES_FEEL}<br>"
            f"➡️ {LINK_COMEDY}<br>"
            "Laughter and light stories are powerful healers 🌸"
        )

    # 🌙 8. Relax / meditation / calm request
    if _has_any(msg, ["relax", "relaxation", "meditate", "calm", "peaceful", "mindfulness", "breathe"]):
        return (
            f"🧘 Let’s relax together, {name}. Try one of these calming choices:<br>"
            f"➡️ {LINK_MINDFUL_VIDEO}<br>"
            f"➡️ {LINK_BREATHING}<br>"
            f"➡️ {_a('https://www.youtube.com/watch?v=ZToicYcHIOU','10-Minute Mindful Breathing 🌿')}<br>"
            "Would you like me to play calming background sounds too?"
        )

    # 💬 9. General emotions (sad, anxious, bored)
    if _has_any(msg, ["sad", "upset", "low", "not good", "angry", "tired", "lonely"]):
        responses = [
            f"I hear you, {name}. It’s okay to feel that way 💚 Try a reset: breathe slowly and listen to {LINK_SPOTIFY_CALM}.",
            f"You’re not alone, {name}. Here’s a 2-min calm session: {LINK_MINDFUL_VIDEO}",
            f"Bad days pass too, {name}. Maybe watch {LINK_COMEDY} to lift your mood 🌤️"
        ]
        return random.choice(responses)

    # 💪 10. Positive moods
    if _has_any(msg, ["good", "happy", "better", "fine", "awesome", "ok now", "okay now"]):
        return f"That’s amazing, {name}! 🌸 Keep that energy alive with {LINK_SPOTIFY_HAPPY} or {LINK_MOVIES_FEEL}."

    # 🧠 11. Motivation / quote / advice
    if _has_any(msg, ["motivate", "quote", "advice", "inspire"]):
        quotes = [
            "🌿 <i>Healing is not about speed — it’s about direction.</i>",
            "💫 <i>Recovery doesn’t mean perfection, it means progress.</i>",
            "🌻 <i>You’ve survived 100% of your bad days — that’s strength.</i>"
        ]
        return random.choice(quotes)

    # 🙋 12. Greetings
    if _has_any(msg, ["hi", "hello", "hey", "morning", "evening"]):
        return f"👋 Hey {name}! How are you feeling today?"

    # 🕊️ 13. Default fallback
    return (
        f"Thanks for sharing, {name}. I’m here to help 🌿<br>"
        "You can ask me for <b>music</b>, <b>games</b>, <b>exercise</b>, or <b>relaxation</b> ideas anytime 💚"
    )











