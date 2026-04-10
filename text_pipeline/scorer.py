# scorer.py

import re
import math
from collections import Counter

# CONFIG
VOWELS = "aeiou"

COMMON_BIGRAMS = {
    "th", "he", "in", "er", "an", "re", "on", "at", "en",
    "nd", "ti", "es", "or", "te", "of", "ed", "is", "it",
    "al", "ar", "st", "to", "nt", "ng", "se", "ha", "as"
}


# METRICS
def entropy(text):
    freq = Counter(text)
    n = len(text)
    return -sum((c/n) * math.log2(c/n) for c in freq.values())


def common_bigram_ratio(text):
    if len(text) < 4:
        return 1

    total = 0
    common = 0

    for i in range(len(text) - 1):
        bg = text[i:i+2]
        total += 1
        if bg in COMMON_BIGRAMS:
            common += 1

    return common / total if total else 1


def max_consonant_run(text):
    max_count = 0
    count = 0

    for c in text:
        if c not in VOWELS and c.isalpha():
            count += 1
            max_count = max(max_count, count)
        else:
            count = 0

    return max_count


# MAIN SCORER
def score_input(text: str) -> float:
    if not text:
        return 0

    text = text.lower()
    score = 100
    words = text.split()

    # structural redundancy
    if len(words) >= 4:
        ratio = len(set(words)) / len(words)
        if ratio < 0.5:
            score -= 20

    # info density
    if words:
        avg_len = sum(len(w) for w in words) / len(words)
        if avg_len < 3:
            score -= 15

    # entropy (more aggressive)
    if len(text) > 12:
        e = entropy(text)
        if e > 4.2:
            score -= 35

    # repeated patterns
    if re.search(r'(.{2,3})\1{2,}', text):
        score -= 40

    # consonant runs (key)
    if max_consonant_run(text) >= 5:
        score -= 40

    # low vowel ratio per word
    for w in words:
        if len(w) >= 6:
            vowels = sum(1 for c in w if c in VOWELS)
            if vowels / len(w) < 0.25:
                score -= 25
                break

    # suspicious single word (very key)
    if len(words) == 1 and len(text) > 8:
        diversity = len(set(text)) / len(text)
        e = entropy(text)

        if diversity > 0.6 and e > 3.5:
            score -= 60

    # unlikely bigrams
    if len(text) > 10:
        ratio_bg = common_bigram_ratio(text)
        if ratio_bg < 0.15:
            score -= 50

    # bonus: useful density
    if any(c.isdigit() for c in text):
        score += 5

    if 2 <= len(words) <= 6:
        score += 5

    # long redundancy
    if len(text) > 150 and len(words) > 10:
        ratio = len(set(words)) / len(words)
        if ratio < 0.6:
            score -= 15

    # FINAL CLAMP
    return max(min(score, 100), 0)