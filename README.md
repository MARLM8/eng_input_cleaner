# Eng Input Cleaner

Lightweight text preprocessing pipeline for cleaning, scoring and compressing user input.

Designed for LLM optimization, noise reduction and token efficiency.

---

## Features

- Text normalization and cleanup
- Noise detection using heuristic scoring
- Input compression (removes low-value words)
- Quality scoring system (0–100)
- Smart truncation for long inputs
- Token reduction tracking using `tiktoken`

---

## Installation

```bash
pip install eng-input-cleaner
```

Or local development:

```bash
pip install -e .
```

---

## Quick Start

```python
from eng-input-cleaner import process

result = process("hello hello I really really need help with this")

print(result)
```

---

## Example Output

```json
{
  "original": "hello hello I really really need help with this",
  "cleaned": "i really need help with this",
  "output": "need help",
  "score": 78,
  "status": "accepted",
  "was_compressed": true,
  "tokens_before": 10,
  "tokens_after": 2,
  "token_reduction": 0.8,
  "token_reduction_pct": "80.00%"
}
```

---

## Pipeline Overview

The system processes text in 4 sequential stages:

```
raw input
    ↓
1. Cleaner     ← normalizes and removes noise
    ↓
2. Scorer      ← evaluates quality on cleaned text (0–100)
    ↓
3. Decision    ← accepts or blocks based on score
    ↓
4. Compressor  ← always runs on accepted text
    ↓
  LLM
```

### 1. Cleaning

- Normalize text (lowercase, symbols, encoding)
- Remove duplicate words and repeated characters
- Filter noise patterns using heuristic scoring
- Collapse redundant symbols

### 2. Scoring

Evaluates the **cleaned** text using:

- Character entropy
- Character diversity
- Vowel ratio
- Common bigram ratio
- Consonant run length
- Cyclic and structural pattern detection

### 3. Decision

- Block low-quality or noisy input
- Accept valid input (short or long)
- Apply smart truncation for very long inputs

### 4. Compression

Runs on every accepted text regardless of score:

- Removes low-value words (articles, weak intensifiers, filler)
- Preserves intent words, negations, question words and structured data

---

## Status Values

| Status | Meaning |
| --- | --- |
| `accepted` | Valid input, normal or long length |
| `accepted_short` | Valid input, short (1–5 words) |
| `blocked_empty` | Empty or whitespace-only input |
| `blocked_low_score` | Quality score below threshold |
| `blocked_noise` | Single long token detected as noise |
| `blocked_low_info` | Too short to carry meaningful information |

---

## Output Fields

| Field | Type | Description |
| --- | --- | --- |
| `original` | `str` | Raw input as received |
| `cleaned` | `str` | After normalization and noise removal |
| `output` | `str \| None` | Final text sent to LLM, `None` if blocked |
| `score` | `float` | Quality score from 0 to 100 |
| `status` | `str` | Pipeline decision result |
| `was_compressed` | `bool` | Whether compression was applied |
| `tokens_before` | `int` | Token count of original input |
| `tokens_after` | `int` | Token count of final output |
| `token_reduction` | `float` | Fractional reduction (e.g. `0.8`) |
| `token_reduction_pct` | `str` | Human-readable reduction (e.g. `"80.00%"`) |

---

## Use Cases

- Preprocessing user input for LLMs
- Reducing token costs
- Filtering spam or noisy text
- Improving prompt quality
- Input validation layer for APIs

---

## Requirements

- Python 3.8+
- `tiktoken`

---

## Project Structure

```
input_cleaner/
├── cleaner.py      ← normalization and noise filtering
├── scorer.py       ← quality scoring (0–100)
├── decision.py     ← accept / block logic
├── compressor.py   ← low-value word removal
└── pipeline.py     ← orchestrates all stages
```

---

## Design Goals

- **Fast** — pure Python, no heavy dependencies
- **Deterministic** — no randomness, same input always produces same output
- **Modular** — each stage is isolated and independently testable
- **Easy to extend** — thresholds and word lists are configurable

---

## License

Apache-2.0

---

## Author

marlon (MARLM8)
