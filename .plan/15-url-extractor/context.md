# #15: Context

## Issue Description

Build `extract_urls(text: str) -> list[str]` in `backend/app/core/preprocessing/url_extractor.py`.

The function runs on raw SMS text **before** `normalize()` so that domain casing, punycode, and percent-encoding are preserved for Phase 1 (URL Checker) analysis.

**Acceptance criteria:**
- Extracts standard `http://` and `https://` URLs from plain text
- Extracts bare domains without protocol (e.g., `bit.ly/abc123`)
- Handles multiple URLs in a single message
- Preserves the original form of each URL (no lowercasing or stripping)
- Returns an empty list for messages with no URLs
- Does not extract email addresses as URLs

## Component Summary

### Current State

`url_extractor.py` exists but contains only a stub:
```python
def extract_urls(text: str) -> list[str]:
    pass
```

`url_checker.py` has a private `extract_urls` method (line 37–40) that covers protocol URLs only via `re.findall(r'https?://[^\s]+', text)`. This is Phase 1 logic and is not replaced by this issue — Phase 0 extraction runs before normalization; Phase 1 receives the already-extracted list.

### Target State

`extract_urls` implements a two-pass approach:

**Pass 1 — Protocol URLs:** regex `https?://[^\s@]+`, then strip trailing punctuation (`.`, `,`, `)`, etc.) that is not structurally part of the URL.

**Pass 2 — Bare domains:** regex anchored with `(?<!\w@)\b`, TLD whitelist to avoid false positives on `2.0`, `node.js`, version strings, etc. Scrubs protocol URL spans first to prevent double-matching.

Known-scam corpus breakdown (from `data/known-scams/known-scams.md`):
- **Protocol URLs (~50%):** `https://purolator.com-payrp.vip/ca`, `https://canada.postscanadacuy.top/ca`, etc.
- **Bare domains (~50%):** `manage-account-detail.com`, `1royalbankomni-manage.com`, `tickets-unsettled-transports-ca.com`, etc.

## Impact & Risk

### Files Changed

- **`backend/app/core/preprocessing/url_extractor.py`** — implement `extract_urls`; add module-level compiled regexes
- **`backend/tests/test_url_extractor.py`** — new test file covering all acceptance criteria plus edge cases

### Dependencies

- **`backend/app/core/preprocessing/normalizer.py`** — `extract_urls` must run before `normalize()` is called; ordering is enforced by the pipeline orchestrator (not this module)
- **`backend/app/core/rules/url_checker.py`** — Phase 1 consumer of the extracted URL list; its own `extract_urls` method is unaffected by this issue

### Pipeline Impact

Phase 0 runs `extract_urls(raw_text)` → bundles result into `artifacts["urls"]` → passes to Phase 1 (`URLChecker`). This issue only implements the function; wiring into `artifacts{}` is the pipeline orchestrator's concern (future issue).
