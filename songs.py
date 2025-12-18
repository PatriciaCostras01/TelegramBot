import random
<<<<<<< HEAD
=======
import unicodedata

>>>>>>> 0ed699c (Update SugarGlitter project)
MOOD_SONGS = {
    "sad": [
        ("Florin Salam – O viață de desfrâu", "https://www.youtube.com/watch?v=YxTUrp_gfYM"),
        ("Adi Minune – Așa sunt zilele mele", "https://www.youtube.com/watch?v=7NE6PFcAckU"),
        ("Nicolae Guță – Amintirea", "https://www.youtube.com/watch?v=8AeR9sgPik8"),
        ("Laura Vass – Te-am iubit dar m-ai mințit", "https://www.youtube.com/watch?v=Lp6TQhNnLFc"),
        ("Denisa – Ce frumoasă-i viața mea", "https://www.youtube.com/watch?v=kqgC6KTQJ0M"),
<<<<<<< HEAD
=======
        ("Nicolae Guță – Mi-ai lasat o floare in glastra", "https://www.youtube.com/watch?v=IrMk66nFWPI&list=RDIrMk66nFWPI&start_radio=1"),
        ("Vali Vijelie – De ce mă minți", "https://www.youtube.com/watch?v=YkXUu0Y3b5I"),
        ("Florin Salam – 7 trandafiri", "https://www.youtube.com/watch?v=Zcq8XpM5hMo&list=RDZcq8XpM5hMo&start_radio=1"),
>>>>>>> 0ed699c (Update SugarGlitter project)
    ],

    "love": [
        ("Nicolae Guță & Sorina – Ce bine ne stă împreună", "https://www.youtube.com/watch?v=nzP8lZ1urxQ"),
        ("Vali Vijelie – Dragostea ta", "https://www.youtube.com/watch?v=FQwVYzY9500"),
        ("Costi Ioniță – Tu ești viața mea", "https://www.youtube.com/watch?v=hV7rEOBz9lI"),
        ("Denisa – Vreau să-mi spui iară că mă iubești", "https://www.youtube.com/watch?v=ZrQ2hYwT5Ks"),
        ("Adi Minune – Mă iubești sau mă minți", "https://www.youtube.com/watch?v=ZoZyZb9FseE"),
<<<<<<< HEAD
=======
        ("Florin Salam & Gabita de la Craiova – Doar dragostea", "https://www.youtube.com/watch?v=E0dKmtZdv7c&list=RDE0dKmtZdv7c&start_radio=1"),
        ("Florin Salam & Printesa de aur – Unii se lauda", "https://www.youtube.com/watch?v=X_ox89CjBOU&list=RDX_ox89CjBOU&start_radio=1"),
>>>>>>> 0ed699c (Update SugarGlitter project)
    ],

    "party": [
        ("Florin Salam – Saint Tropez", "https://www.youtube.com/watch?v=KUH-1NHdJv8"),
        ("Vali Vijelie – Banii, banii", "https://www.youtube.com/watch?v=zjv1e6dO4E4"),
        ("Nicolae Guță – Până dimineață", "https://www.youtube.com/watch?v=L1zGQ-ca9Vc"),
        ("Liviu Guță – Fata mea", "https://www.youtube.com/watch?v=yLJeYf1Q14c"),
        ("Jean de la Craiova – Rău mă dor ochii mă dor", "https://www.youtube.com/watch?v=YtasFr9YJgw"),
<<<<<<< HEAD
=======
        ("Adi de la Vâlcea – Lume, lume", "https://www.youtube.com/watch?v=H1pX2k1bXME"),
        ("Florin Salam & Ionut Sturzea – Ma gandesc la tine", "https://www.youtube.com/watch?v=L-Zi_tTur9k&list=RDL-Zi_tTur9k&start_radio=1"),
>>>>>>> 0ed699c (Update SugarGlitter project)
    ],

    "chill": [
        ("Denisa – Mă doare la inimioară", "https://www.youtube.com/watch?v=2Y0Oyw5R7Lw"),
        ("Sorina Ceugea – Nu plânge inimioară", "https://www.youtube.com/watch?v=dw_jF8VE3Sk"),
        ("Liviu Guță – Ești frumoasă, fata mea", "https://www.youtube.com/watch?v=sa7B8C2YtXw"),
        ("Adi de la Vâlcea – Să-mi cânte fanfara", "https://www.youtube.com/watch?v=Qn0q2qp6j3s"),
        ("Nicolae Guță – Ce bine ne stă împreună (slow version)", "https://www.youtube.com/watch?v=Ngdn0M3Cl7I"),
    ],

<<<<<<< HEAD
        "happy": [
=======
    "happy": [
>>>>>>> 0ed699c (Update SugarGlitter project)
        ("Vali Vijelie – Norocul meu", "https://www.youtube.com/watch?v=Ubbmxa0dzM0"),
        ("Florin Salam – Traieste-ti viata", "https://www.youtube.com/watch?v=YxTUrp_gfYM"),
        ("Liviu Guță – Viața e frumoasă", "https://www.youtube.com/watch?v=PGXJ1ANu1vU"),
        ("Adi Minune – Fericirea mea", "https://www.youtube.com/watch?v=3i9aZkY5ZVU"),
        ("Nicolae Guță – Hai să trăim bine", "https://www.youtube.com/watch?v=b5RQ-gQwp2o"),
    ],
}

MOOD_ALIASES = {
    "sad": ["sad", "trist", "suparat", "down", "plang", "plâng", "plângând", "broken", "jale"],
    "love": ["love", "dragoste", "iubire", "in love", "romantic", "amor", "heart"],
    "party": ["party", "chef", "petrecere", "dans", "dance", "let’s go", "distractie", "hype"],
    "chill": ["chill", "relaxed", "calm", "linistit", "obosit", "ok", "fine", "doarme", "sleepy"],
    "happy": ["happy", "fericit", "bucuros", "bine", "yay", "joy"],
}


def normalize_mood(text: str) -> str | None:
    if not text:
        return None
<<<<<<< HEAD
    t = text.lower().strip()
=======
    # Normalize and remove diacritics for more robust matching
    t = text.lower().strip()
    t = unicodedata.normalize("NFKD", t)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
>>>>>>> 0ed699c (Update SugarGlitter project)

    if t in MOOD_SONGS:
        return t

<<<<<<< HEAD
    for mood, aliases in MOOD_ALIASES.items():
        if any(word in t for word in aliases):
            return mood
=======
    # Token-aware matching: check aliases as whole words first
    tokens = set(t.split())
    for mood, aliases in MOOD_ALIASES.items():
        for alias in aliases:
            # normalize alias the same way
            a = unicodedata.normalize("NFKD", alias.lower().strip())
            a = "".join(ch for ch in a if not unicodedata.combining(ch))
            if a in tokens or a == t or a in t:
                return mood
>>>>>>> 0ed699c (Update SugarGlitter project)

    return None


def pick_song_for_mood(mood: str):
    mood = mood.lower().strip()
    if mood not in MOOD_SONGS:
        return None
    return random.choice(MOOD_SONGS[mood])