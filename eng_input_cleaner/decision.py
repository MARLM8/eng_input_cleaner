import re


def smart_truncate(text: str, max_words: int = 40) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    result = []
    total = 0

    for sentence in sentences:
        w = len(sentence.split())
        if total + w <= max_words:
            result.append(sentence)
            total += w
        else:
            break

    if not result:
        return " ".join(text.split()[:max_words])

    return " ".join(result)


def decide_input(text: str, score: float):
    if not text or not text.strip():
        return None, "blocked_empty"

    words = text.split()
    word_count = len(words)
    length = len(text)

    if score < 35:
        return None, "blocked_low_score"

    if word_count == 1 and length < 4:
        return None, "blocked_low_info"

    if word_count == 1 and length > 12:
        if score >= 55:
            return text, "accepted_short"
        return None, "blocked_noise"

    if word_count <= 5:
        if score >= 65:
            return text, "accepted_short"
        if score >= 45:
            return text, "accepted_short"   
        return None, "blocked_low_score"


    needs_truncation = length > 300 or word_count > 50
    if needs_truncation:
        text = smart_truncate(text, max_words=40)
        words = text.split()
        word_count = len(words)
        length = len(text)

        if word_count < 3:
            return text, "accepted"        

    if score >= 78:
        return text, "accepted"

    if score >= 50:
        return text, "accepted"           

    if score >= 35 and word_count > 8:
        return text, "accepted"           

    return None, "blocked_low_score"