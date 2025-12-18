from songs import normalize_mood, pick_song_for_mood

samples = ['fericit', 'fericIT', 'fericită', 'happy', 'trist', 'suparat', 'plâng', 'plang', 'in love', 'chef', 'calm']

for s in samples:
    mood = normalize_mood(s)
    song = pick_song_for_mood(mood) if mood else None
    print(f"input={s!r} -> mood={mood!r} -> song={(song[0] if song else None)!r}")
