# Text Pipeline

Lightweight text preprocessing pipeline for cleaning, scoring and compressing user input.

Designed for LLM optimization, noise reduction and token efficiency.

---

## Features

* Text normalization and cleanup
* Noise detection using heuristic scoring
* Input compression (removes low-value words)
* Quality scoring system (0–100)
* Smart truncation for long inputs
* Token reduction tracking using `tiktoken`

---

## Installation

```bash
pip install input_cleaner
```

Or local development:

```bash
pip install -e .
```

---

## Quick Start

```python
from input_cleaner import process

result = process("hello hello I really really need help with this")

print(result)
```

---

## Example Output

```json
{
  "original": "hello hello I really really need help with this",
  "cleaned": "hello i really need help with this",
  "compressed": "need help this",
  "score": 78,
  "status": "compress",
  "output": "need help this",
  "token_reduction": 0.32
}
```

---

## Pipeline Overview

The system processes text in 4 stages:

1. **Cleaning**

   * Normalize text (lowercase, symbols)
   * Remove duplicates and noise patterns

2. **Compression**

   * Remove weak or redundant words
   * Preserve important tokens

3. **Scoring**

   * Evaluate text quality using:

     * entropy
     * character diversity
     * vowel ratio
     * pattern detection

4. **Decision**

   * Block low-quality input
   * Compress medium-quality input
   * Accept high-quality input
   * Truncate long input if needed

---

## Status Values

| Status              | Meaning               |
| ------------------- | --------------------- |
| `blocked_empty`     | Empty input           |
| `blocked_low_score` | Low quality score     |
| `blocked_noise`     | Likely random string  |
| `blocked_low_info`  | Too short / low value |
| `accepted_short`    | Short but valid       |
| `compress`          | Needs compression     |
| `truncated_smart`   | Long input trimmed    |
| `accepted`          | Fully valid           |

---

## Use Cases

* Preprocessing user input for LLMs
* Reducing token costs
* Filtering spam or noisy text
* Improving prompt quality
* Input validation layer for APIs

---

## Requirements

* Python 3.8+
* `tiktoken`

---

## Project Structure

```bash
text_pipeline/
├── cleaner.py
├── compressor.py
├── scorer.py
├── decision.py
└── pipeline.py
```

---

## Design Goals

* Fast (pure Python, no heavy dependencies)
* Deterministic (no randomness)
* Modular (each step isolated)
* Easy to extend

---

## Roadmap (optional)

* Add trigram scoring
* Language detection
* Configurable thresholds
* FastAPI wrapper
* Streaming support

---

## License

Apache-2.0

---

## Author

marlon (MARLM8)
