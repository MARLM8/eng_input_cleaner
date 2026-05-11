# cleaner.py
import re
import math
from collections import Counter

# CONFIG PANEL
ALLOWED = r",\.\?\(\)\/\-\+\"=<>\:@%#"

CONFIG = {
    # Normalization
    "lowercase": True,
    "replace_semicolon": True,
    "replace_quotes": True,

    # Duplicates
    "remove_duplicate_words": True,

    # Repeats
    "max_char_repetition": 4,

    # Heuristics
    "enable_noise_filter": True,
    "min_word_length": 12,

    # Metrics
    "diversity_threshold": 0.30,
    "entropy_threshold": 3.8,
    "min_vowel_ratio": 0.20,

    # Suspicious patterns
    "keyboard_patterns": [
    "qwert", "werty", "ertyu", "rtyui", "tyuio", "yuiop", 
    "asdfg", "sdfgh", "dfghj", "fghjk", "ghjkl",         
    "zxcvb", "xcvbn", "cvbnm",                             
    "qazws", "wsxed", "edcrf", "rfvtg", "tgbyh",           
    "12345", "23456", "34567", "45678", "56789", "67890",],
    "weird_bigrams": [
    "jh", "jk", "jl", "jm", "jn", "jp", "jr", "js", "jt", "jv", "jw", 
    "kj", "kq", "kz",
    "qk", "qb", "qc", "qd", "qf", "qg", "qh", "qj", "qm", "qp", "qt", "qv", "qw", "qx", "qy",
    "vb", "vd", "vf", "vg", "vj", "vk", "vm", "vp", "vq", "vt", "vw", "vx", "vz",
    "wk", "wj", "wq", "wv", "wx", "wz",
    "xj", "xk",
    "zx", "zj", "zk", "zq",],

    # Scoring
    "score_threshold": 4,

    # Action
    "truncate_noise": True,
    "truncate_length": 8,

    # Artificial lists
    "max_commas": 5,

    # Final cleanup
    "collapse_symbols": True,
    "normalize_spaces": True,
}


# METRICS
def entropy(p):
    freq = Counter(p)
    n = len(p)
    return -sum((c/n) * math.log2(c/n) for c in freq.values())


def vowel_ratio(p):
    vowels = re.findall(r'[aeiouáéíóú]', p)
    return len(vowels) / len(p) if p else 0


# NOISE CLASSIFIER
def noise_score(p, cfg):
    score = 0

    if len(p) < cfg["min_word_length"]:
        return 0

    if any(c.isdigit() for c in p):
        return 0

    # Diversity
    diversity = len(set(p)) / len(p)
    if diversity < cfg["diversity_threshold"]:
        score += 2

    # High entropy 
    if entropy(p) > cfg["entropy_threshold"]:
        score += 1

    # Low vowels
    if vowel_ratio(p) < cfg["min_vowel_ratio"]:
        score += 1

    # Structural repeats
    if re.search(r'(.{2,4})\1{2,}', p):
        score += 2

    # Keyboard patterns
    if any(x in p for x in cfg["keyboard_patterns"]):
        score += 2

    # Weird bigrams
    if any(bg in p for bg in cfg["weird_bigrams"]):
        score += 1

    return score


def reduce_if_noise(match, cfg):
    p = match.group(0)
    score = noise_score(p, cfg)

    if score >= cfg["score_threshold"]:
        if cfg["truncate_noise"]:
            return p[:cfg["truncate_length"]]
        return ""

    return p


# MAIN FILTER
def filter_input(text: str) -> str:
    cfg = CONFIG

    # Normalization
    if cfg["lowercase"]:
        text = text.lower()

    if cfg["replace_semicolon"]:
        text = text.replace(";", ",")

    if cfg["replace_quotes"]:
        text = text.replace("'", '"')

    text = re.sub(r'[\[\{]', '(', text)
    text = re.sub(r'[\]\}]', ')', text)

    # Base filter
    text = re.sub(
        rf'[^a-záéíóúñüäëïöâêîôûàèìòù0-9\s{ALLOWED}]',
        '',
        text
    )

    # Duplicates
    if cfg["remove_duplicate_words"]:
        text = re.sub(r'\b(\w+)([\s.,]+\1\b)+', r'\1', text)

    # Repeats
    text = re.sub(
        rf'(.)\1{{{cfg["max_char_repetition"]},}}',
        r'\1',
        text
    )

    # Weird patterns
    text = re.sub(
        r'([<>\W])([a-z0-9])(?:\1\2){2,}',
        r'\2',
        text
    )

    # Advanced heuristic
    if cfg["enable_noise_filter"]:
        text = re.sub(
            r'\b[a-záéíóúñüäëïöâêîôûàèìòù]{%d,}\b' % cfg["min_word_length"],
            lambda m: reduce_if_noise(m, cfg),
            text
        )

    # Artificial lists
    if text.count(",") > cfg["max_commas"]:
        text = re.sub(
            r'\b([a-z0-9])(?:,[a-z0-9]){3,}\b',
            r'\1',
            text
        )

    # Collapse symbols
    if cfg["collapse_symbols"]:
        text = re.sub(
            rf'([{ALLOWED}])(\s*[{ALLOWED}])+',
            r'\1',
            text
        )

    # Spaces
    if cfg["normalize_spaces"]:
        text = re.sub(r'\s+', ' ', text).strip()

    return text