# pipeline.py

from .cleaner import filter_input
from .scorer import score_input
from .decision import decide_input
from .compressor import compress_input
import tiktoken


def process(text: str):
    original = text

    cleaned = filter_input(original)
    compressed = compress_input(cleaned)

    score = score_input(cleaned)

    output, status = decide_input(compressed, score)

    # tiktoken (measure token reduction)
    enc = tiktoken.encoding_for_model("gpt-4o-mini")  # or your model
    tokens_before = len(enc.encode(original))
    tokens_after = len(enc.encode(output)) if output else 0

    return {
        "original": original,
        "cleaned": cleaned,
        "compressed": compressed,
        "score": score,
        "status": status,
        "output": output,
        "token_reduction": (
            1 - (tokens_after / tokens_before)
            if tokens_before > 0 else 0
        )
    }
