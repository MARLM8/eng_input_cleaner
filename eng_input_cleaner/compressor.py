import re

KEEP_ALWAYS = {
    # Negations
    "no", "not", "never", "nor", "neither",
    # Logical connectors
    "and", "or", "but", "because", "although",
    "if", "then", "so", "yet",
    # Quantifiers / focus
    "all", "any", "every", "none",
    "only", "just", "even", "also",
    # Question words
    "who", "what", "where", "when", "why", "how", "which",
    # Comparators
    "more", "less", "better", "worse", "than",
    # References
    "this", "that", "those", "these", "same",
    # Intent modals
    "need", "want", "must", "should", "would", "could", "can",
}

ALWAYS_REMOVE = {
    # Chat noise (zero semantic value)
    "hello", "hey", "hi", "thanks", "thank",
    "please", "pls", "alright",
    # Filler
    "well", "basically", "literally", "actually",
    # Weak intensifiers
    "very", "quite", "really", "super", "much",
}

OPTIONAL_REMOVE = {
    # Articles
    "the", "a", "an", "some",
    # Weak prepositions (inferable from context)
    "of", "in", "on", "by", "with",
    # Pronouns 
    "it", "its",
}

LOW_VALUE_SHORT = {"ok", "eh", "ah", "uh", "um", "oh"}


def compress_input(text: str) -> str:
    if not text:
        return ""

    text = text.lower()

    # Remove consecutive duplicates
    text = re.sub(r'\b(\w+)(\s+\1\b)+', r'\1', text)

    words = text.split()
    result = []

    for w in words:

        # KEEP_ALWAYS 
        if w in KEEP_ALWAYS:
            result.append(w)
            continue

        # ALWAYS_REMOVE 
        if w in ALWAYS_REMOVE:
            continue

        # Low-value filler shorts
        if w in LOW_VALUE_SHORT:
            continue

        # Structured data 
        if any(c.isdigit() for c in w):
            result.append(w)
            continue

        # Noise patterns
        if re.search(r'(.{2,3})\1{2,}', w):
            continue

        # OPTIONAL_REMOVE
        if w in OPTIONAL_REMOVE:
            if len(words) > 6:  
                continue
            else:
                result.append(w)
                continue

        # DEFAULT keep
        result.append(w)

    return " ".join(result)