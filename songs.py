import random
MOOD_SONGS = {
    "sad": [
        ("Florin Salam – O viață de desfrâu", "https://www.youtube.com/watch?v=YxTUrp_gfYM"),
        ("Adi Minune – Așa sunt zilele mele", "https://www.youtube.com/watch?v=7NE6PFcAckU"),
        ("Nicolae Guță – Amintirea", "https://www.youtube.com/watch?v=8AeR9sgPik8"),
        ("Laura Vass – Te-am iubit dar m-ai mințit", "https://www.youtube.com/watch?v=Lp6TQhNnLFc"),
        ("Denisa – Ce frumoasă-i viața mea", "https://www.youtube.com/watch?v=kqgC6KTQJ0M"),
    ],

    "love": [
        ("Nicolae Guță & Sorina – Ce bine ne stă împreună", "https://www.youtube.com/watch?v=nzP8lZ1urxQ"),
        ("Vali Vijelie – Dragostea ta", "https://www.youtube.com/watch?v=FQwVYzY9500"),
        ("Costi Ioniță – Tu ești viața mea", "https://www.youtube.com/watch?v=hV7rEOBz9lI"),
        ("Denisa – Vreau să-mi spui iară că mă iubești", "https://www.youtube.com/watch?v=ZrQ2hYwT5Ks"),
        ("Adi Minune – Mă iubești sau mă minți", "https://www.youtube.com/watch?v=ZoZyZb9FseE"),
    ],

    "party": [
        ("Florin Salam – Saint Tropez", "https://www.youtube.com/watch?v=KUH-1NHdJv8"),
        ("Vali Vijelie – Banii, banii", "https://www.youtube.com/watch?v=zjv1e6dO4E4"),
        ("Nicolae Guță – Până dimineață", "https://www.youtube.com/watch?v=L1zGQ-ca9Vc"),
        ("Liviu Guță – Fata mea", "https://www.youtube.com/watch?v=yLJeYf1Q14c"),
        ("Jean de la Craiova – Rău mă dor ochii mă dor", "https://www.youtube.com/watch?v=YtasFr9YJgw"),
    ],

    "chill": [
        ("Denisa – Mă doare la inimioară", "https://www.youtube.com/watch?v=2Y0Oyw5R7Lw"),
        ("Sorina Ceugea – Nu plânge inimioară", "https://www.youtube.com/watch?v=dw_jF8VE3Sk"),
        ("Liviu Guță – Ești frumoasă, fata mea", "https://www.youtube.com/watch?v=sa7B8C2YtXw"),
        ("Adi de la Vâlcea – Să-mi cânte fanfara", "https://www.youtube.com/watch?v=Qn0q2qp6j3s"),
        ("Nicolae Guță – Ce bine ne stă împreună (slow version)", "https://www.youtube.com/watch?v=Ngdn0M3Cl7I"),
    ],

        "happy": [
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
    t = text.lower().strip()

    if t in MOOD_SONGS:
        return t

    for mood, aliases in MOOD_ALIASES.items():
        if any(word in t for word in aliases):
            return mood

    return None


def pick_song_for_mood(mood: str):
    mood = mood.lower().strip()
    if mood not in MOOD_SONGS:
        return None
    return random.choice(MOOD_SONGS[mood])