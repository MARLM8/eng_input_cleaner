# pipeline.py

from .cleaner import filter_input
from .scorer import score_input
from .decision import decide_input
from .compressor import compress_input
import tiktoken
from functools import lru_cache


@lru_cache(maxsize=8)
def _get_encoder(model: str):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")


def process(text: str, model: str = "gpt-4o-mini") -> dict:

    # Early exit
    if not text or not text.strip():
        return {
            "original":          text,
            "output":            None,
            "status":            "blocked_empty",
            "score":             0,
            "was_compressed":    False,
            "tokens_before":     0,
            "tokens_after":      0,
            "token_reduction":   0,
            "token_reduction_pct": "0.00%",
        }

    original = text

    cleaned = filter_input(original)

    score = score_input(cleaned)

    output, status = decide_input(cleaned, score)

    if output is not None:
        output = compress_input(output)

    enc = _get_encoder(model)

    tokens_before = len(enc.encode(original))
    tokens_after  = len(enc.encode(output)) if output else 0

    reduction = 1 - (tokens_after / tokens_before) if tokens_before > 0 else 0

    return {
        "original":            original,
        "cleaned":             cleaned,
        "output":              output,
        "status":              status,
        "score":               score,
        "tokens_before":       tokens_before,
        "tokens_after":        tokens_after,
        "token_reduction":     round(reduction, 4),
        "token_reduction_pct": f"{reduction * 100:.2f}%",
    }