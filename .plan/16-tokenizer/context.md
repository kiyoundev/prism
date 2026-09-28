# Issue #16: Context

## Issue Description

Build `backend/app/core/preprocessing/tokenizer.py` with three functions:

- `tokenize(text: str) -> list[str]` — splits into word tokens (alphanumeric only, lowercased, no punctuation, no extra whitespace)
- `ngrams(tokens: list[str], n: int) -> list[str]` — generates n-gram phrases joined by spaces
- `get_ngrams(tokens: list[str]) -> list[str]` — returns bi-grams + tri-grams combined

Outputs are consumed by the brand/category extractor (Phase 0) and the Phase 2 TF-IDF pipeline.

Docs: `.docs/rule_engine.md` — Phase 0: Tokenization & N-grams

## Component / Route Summary

### Current State

`backend/app/core/preprocessing/` contains:
- `normalizer.py` — lowercases, strips punctuation, handles unicode/homoglyphs/zero-width chars
- `url_extractor.py` — two-pass regex URL extraction
- `__init__.py` — empty

No tokenizer exists. Brand/category extraction and TF-IDF are currently blocked on this module.

### Target State

New file `tokenizer.py` providing the three functions above. `tokenize` receives text that may or may not be pre-normalized; it defensively lowercases and filters to alphanumeric tokens. `ngrams` and `get_ngrams` operate on already-tokenized token lists.

## Impact & Risk

### Files Changed
- **`backend/app/core/preprocessing/tokenizer.py`** — new file, three pure functions
- **`backend/tests/test_tokenizer.py`** — new test file covering all acceptance criteria + edge cases

### Dependencies
- **`normalizer.py`** — `tokenize` is downstream of `normalize()` in the pipeline; its input is already lowercased and punctuation-stripped, but `tokenize` lowercases defensively
- **brand/category extractor** — will import `tokenize` and `get_ngrams` once implemented
- **Phase 2 TF-IDF pipeline** — will import `tokenize` and `get_ngrams`

### New Dependencies
None — implementation uses only stdlib `re`.
