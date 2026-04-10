# Compressor.py

import re

# 🔹 CONFIG
ALWAYS_REMOVE = {
    # chat noise
    "hello", "hey", "ok", "alright", "well",
    "thanks", "please", "pls",

    # articles
    "the", "a", "an", "some"
}

OPTIONAL_REMOVE = {
    # weak verbs
    "need", "want", "wish", "can", "could",
    "would", "like",

    # prepositions
    "of", "from", "to", "in", "on", "by", "for", "with", "without",

    # pronouns
    "me", "you", "him", "her", "us", "them", "it",

    # intensifiers
    "very", "much", "quite", "really", "super"
}

KEEP_ALWAYS = {
    # negations
    "no", "never",

    # comparators
    "more", "less", "better", "worse",

    # logical connectors
    "but", "because", "although", "if", "then",

    # references
    "this", "that", "those", "same"
}


# COMPRESSOR
def compress_input(text: str) -> str:
    if not text:
        return ""

    text = text.lower()

    # remove consecutive duplicates
    text = re.sub(r'\b(\w+)(\s+\1\b)+', r'\1', text)

    words = text.split()
    result = []

    for w in words:

        # KEEP_ALWAYS → always keep
        if w in KEEP_ALWAYS:
            result.append(w)
            continue

        # ALWAYS_REMOVE → always drop
        if w in ALWAYS_REMOVE:
            continue

        # STRUCTURED DATA
        if any(c.isdigit() for c in w):
            result.append(w)
            continue

        # VERY SHORT WORDS
        if len(w) < 3:
            continue

        # REPEATED PATTERNS (noise)
        if re.search(r'(.{2,3})\1{2,}', w):
            continue

        # OPTIONAL_REMOVE
        if w in OPTIONAL_REMOVE:
            # drop only if enough context
            if len(words) > 3:
                continue
            else:
                result.append(w)
                continue

        # DEFAULT → keep
        result.append(w)

    return " ".join(result)