# decision.py

def decide_input(text: str, score: float):

    if not text:
        return None, "blocked_empty"

    words = text.split()
    word_count = len(words)
    length = len(text)

    # HARD BLOCK
    if score < 40:
        return None, "blocked_low_score"

    # typical noise (random strings)
    if word_count == 1 and length > 12:
        return None, "blocked_noise"

    # too short input (low value)
    if word_count <= 1 and length < 4:
        return None, "blocked_low_info"

    # SHORT USEFUL TEXT (KEEP)
    if word_count <= 4 and score >= 70:
        return text, "accepted_short"

    # NEED COMPRESSION
    if score < 80:
        return text, "compress"

    # LONG TEXT → SMART TRIM
    if length > 180 or word_count > 30:
        useful_words = words[:40]
        return " ".join(useful_words), "truncated_smart"

    # ACCEPTED
    return text, "accepted"
