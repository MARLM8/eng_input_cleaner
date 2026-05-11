import re
import math
from collections import Counter

VOWELS = "aeiouáéíóú"

COMMON_BIGRAMS = {
    "th", "he", "in", "er", "an", "re", "on", "at", "en",
    "nd", "ti", "es", "or", "te", "of", "ed", "is", "it",
    "al", "ar", "st", "to", "nt", "ng", "se", "ha", "as"
}


def entropy(text):
    freq = Counter(text)
    n = len(text)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


def common_bigram_ratio(text):
    if len(text) < 4:
        return 1.0
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]
    common = sum(1 for bg in bigrams if bg in COMMON_BIGRAMS)
    return common / len(bigrams)


def has_cyclic_pattern(text: str, min_len: int = 2, max_len: int = 6) -> bool:
    for length in range(min_len, min(max_len + 1, len(text) // 2 + 1)):
        pattern = text[:length]
        if text.count(pattern) >= 3:
            return True
    return False


def max_consonant_run(text):
    max_run = count = 0
    for c in text:
        if c.isalpha() and c not in VOWELS:
            count += 1
            max_run = max(max_run, count)
        else:
            count = 0
    return max_run


def vowel_ratio(word):
    if not word:
        return 1.0
    return sum(1 for c in word if c in VOWELS) / len(word)


def score_input(text: str) -> float:
    if not text:
        return 0.0

    text = text.lower().strip()
    words = text.split()
    n_words = len(words)

    if n_words == 0:
        return 0.0

    score = 100.0

    if n_words >= 6:                       
        unique_ratio = len(set(words)) / n_words
        if unique_ratio < 0.35:            
            score -= 15

    if n_words >= 3:
        avg_len = sum(len(w) for w in words) / n_words
        if avg_len < 2.5:                    
            score -= 10

    if len(text) > 15:                    
        e = entropy(text)
        if e > 4.3:                         
            score -= 25

    if re.search(r'(.{2,3})\1{2,}', text):
        score -= 35

    if n_words == 1 and len(text) > 10:
        vr = vowel_ratio(text)
        if vr > 0.60:         
            score -= 20

    if max_consonant_run(text) >= 7:
        score -= 30

    low_vowel_words = [
        w for w in words
        if len(w) >= 8
        and vowel_ratio(w) < 0.18
    ]
    if low_vowel_words:
        score -= min(len(low_vowel_words) * 10, 25)

    if n_words == 1 and len(text) > 10:
        div = len(set(text)) / len(text)
        e = entropy(text)
        vr = vowel_ratio(text)
        if sum([div > 0.75, e > 3.8, vr < 0.15]) >= 2:
            score -= 40

    if len(text) > 8:
        ratio_bg = common_bigram_ratio(text)
        if ratio_bg < 0.12:                  
            score -= 30

    if len(text) > 150 and n_words > 10:
        unique_ratio = len(set(words)) / n_words
        if unique_ratio < 0.50:             
            score -= 10

    if n_words <= 2 and len(text) > 10:
        if has_cyclic_pattern(text):
            score -= 25

    # BONUS

    if any(c.isdigit() for c in text):
        score += 8

    if 3 <= n_words <= 15:
        score += 8

    if len(text) > 15 and n_words > 1:
        if common_bigram_ratio(text) >= 0.25:
            score += 5

    if n_words > 1 or len(text) > 12:
        if 0.30 <= vowel_ratio(text.replace(" ", "")) <= 0.55:
            score += 5

    return round(max(min(score, 100), 0), 2)