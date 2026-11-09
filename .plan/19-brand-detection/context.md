# Issue #19: Context

## Issue Description

Implement brand detection in `backend/app/core/rules/category_extractor.py`. Given the Phase 0 `artifacts{}`, determine which brand the message claims to be from, using the brand named in the text and the brand a link belongs to. The brand (and its category) feeds #22 (brand-domain mismatch), #20 (category resolution), #26 (rule score), Phase 2 features and the Phase 3 prompt.

Original issue: `.docs/issues.md` Issue #19, docs `.docs/rule_engine.md` — Category Extraction Strategy: Brand Detection. The acceptance criteria were amended during planning (see Design Decisions).

## Design Decisions (from planning session)

| # | Decision | Reason |
|---|----------|--------|
| 1 | Rewrite `category_extractor.py` clean; keep the filename | #20 builds on it. The prototype has a duplicate `normalize`/`tokenize`, import-time side effects (loads `seed_scams.json`, downloads NLTK data) and a `scripts.json_loader` import from outside `backend/` |
| 2 | Slugs use hyphens (`canada-post`) | `brand_variants.json` and `url_checker.py` (`slug.replace("-", "")`) already do. The `canada_post` wording in the issue is stale |
| 3 | URL brand matching uses `domains` in `brand_variants.json`; delete `allowed_domains.json` and merge its content in | `allowed_domains.json` has no brand mapping and lacks `canadapost.ca`. `brand_variants.json` is the extensible source |
| 4 | Match brand aliases on the **token list**, not the `ngrams` list | `ngrams` holds only 2–3 word phrases; `united states postal service` has 4 |
| 5 | Matching order: exact spaced sequence, exact joined form, then fuzzy fallback | The normalizer deletes punctuation, so `Canada-Post` becomes the single token `canadapost` |
| 6 | Fuzzy only for aliases of 6+ characters (spaces removed), brand threshold **85**; shorter aliases are exact-only | Short aliases fuzzy-match common words (`puro` vs `pro` scores 86) |
| 7 | Leave `fuzzy_match`'s default threshold at 80; brand detection passes its own 85 | #17's own examples score below 85 (`amaz0n` 83, `f3dex` 80), so the "85" in the docs is stale |
| 8 | `brand_slug` is the winner; also store `text_brand_slug` and `url_brand_slug` | #22 needs the text-claimed brand even when a link's brand wins |
| 9 | `extract()` calls `detect_brand`; `detect_brand` is a pure function that returns fields | Docs list brand extraction as step 4 of Phase 0; pure functions are easier to test |
| 10 | Cached loader `get_brand_index()` (`lru_cache`), path relative to the module, validated; called at FastAPI startup | No import-time side effects, no `scripts/` dependency, fails fast on bad config |
| 11 | `tldextract` uses its bundled suffix snapshot (no network) | Deterministic and offline |
| 12 | Confidence: url 1.0, exact 0.9, leet 0.85 (#19.5), fuzzy 0.8, none 0.0, in one constants table | Docs give 1.0 and 0.9; the rest are chosen |
| 13 | Ties: longest alias wins, then earliest in text; with several links, first link wins and all are kept in a list | Deterministic output |

## Component / Route Summary

### Current State

- `backend/app/core/rules/category_extractor.py` (162 lines) is a prototype: its own `normalize()` and `tokenize()` copies, `build_brand_index()` that reads only the `"delivery"` key, `extract_url()` that prints, `setup_nltk_data()` and `load_json("backend/data/seed_scams.json")` run at import, and `from scripts.json_loader import load_json`.
- `backend/app/core/rules/config/brand_variants.json` has only a `delivery` group: canada-post, purolator, fedex, ups, usps, dhl, each with `slug`, `name`, `aliases`, `domains`.
- `backend/app/core/rules/config/allowed_domains.json` groups bare domains by category (delivery, banking, government). No code reads it.
- `backend/app/core/preprocessing/extractor.py` `extract()` returns `brand_slug: None` and `category: "unknown"` as placeholders (#18).
- `backend/app/core/preprocessing/tokenizer.py` has `fuzzy_match(tokens, candidates, threshold=80)`, which compares a candidate only with phrases of the same word count.
- `backend/tests/test_category_extractor.py` has 7 tests that cover only the prototype's duplicate `normalize()`.
- `backend/app/main.py` has no startup hook yet.

### Target State

- `category_extractor.py` contains only brand detection: `get_brand_index()` (cached, validated), `detect_brand(artifacts) -> dict`, and named constants (minimum fuzzy alias length, fuzzy threshold, confidence table).
- `artifacts{}` gains: `text_brand_slug`, `url_brand_slug`, `brand_match_type` (`url | exact | fuzzy | None`; `leet` arrives in #19.5), `brand_confidence`, plus the existing `brand_slug` and `category` now filled in.
- `brand_variants.json` is the single brand and domain source: banking and government groups added, `canada.ca` under a government brand.

Example output for `"Canada Post: parcel held. Pay at canadapost.ca/track"`:

```python
{
  "brand_slug": "canada-post", "category": "delivery",
  "text_brand_slug": "canada-post", "url_brand_slug": "canada-post",
  "brand_match_type": "url", "brand_confidence": 1.0,
}
```

## Impact & Risk

### Files Changed
- **`backend/app/core/rules/category_extractor.py`** — rewritten (see Target State)
- **`backend/app/core/rules/config/brand_variants.json`** — add `banking` (rbc, td, scotiabank) and `government` (cra, government-of-canada) groups with domains from `allowed_domains.json`; short aliases `td` and `cra` included, to be reviewed later
- **`backend/app/core/rules/config/allowed_domains.json`** — deleted
- **`backend/app/core/preprocessing/extractor.py`** — call `detect_brand` and merge its fields
- **`backend/app/main.py`** — call `get_brand_index()` at startup (FastAPI lifespan)
- **`backend/tests/test_category_extractor.py`** — rewritten for brand detection
- **`backend/tests/test_normalizer.py`** — new; receives the 5 prototype normalize tests that pass on the real normalizer
- **`backend/tests/test_extractor.py`** — extended for the new fields
- **`.docs/issues.md`** — correct #19 (slug, data source, ngrams, amended criteria), #21 and #61 (`allowed_domains.json` references), #17 (stale threshold 85), #22 (use `text_brand_slug`)
- **`.docs/prd.md`, `.docs/overview.md`, `.docs/architecture/architecture.md`, `.docs/architecture/source-tree.md`, `.docs/architecture/coding-standards.md`** — remove `allowed_domains.json` mentions

### Dependencies
- **`app.core.preprocessing.tokenizer.fuzzy_match`** — reused for spaced aliases against n-grams; its default stays 80
- **`rapidfuzz.fuzz.ratio`** — used directly for joined aliases against single tokens
- **`tldextract`** — registered-domain extraction for URL matching
- **`url_checker.py`** — builds its own brand-to-domains map from the same JSON structure; the structure must stay compatible
- **#22 / #20 / #26** — consume `brand_slug`, `text_brand_slug`, `url_brand_slug`, `category`

### New Dependencies
None. `tldextract`, `rapidfuzz` and `nltk` are already pinned in `requirements.txt`.

### Breaking Changes
- `allowed_domains.json` is removed (no code reads it today)
- The prototype's module-level names (`BRANDS`, `SEED_MESSAGES`, `normalize`, `tokenize`, `extract_url`, `build_brand_index`) disappear; only `test_category_extractor.py` imported them
- Two of the 7 prototype normalize tests assert whitespace collapsing, which the real normalizer does not do (see challenges)
