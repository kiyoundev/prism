# Issue #19: Implementation

## Steps

### 1. Setup
- [x] `git switch -c feature/19-brand-detection` from an up-to-date `main`
- [x] Run `pytest` and `ruff check backend` to record the starting state (74 tests passing)

### 2. Config migration (commit 1)
- [x] Add `banking` group to `brand_variants.json`: `rbc` (`rbc.com`), `td` (`td.com`), `scotiabank` (`scotiabank.com`), each with `slug`, `name`, `aliases`, `domains`
- [x] Add `government` group: `cra` (`cra-arc.gc.ca`) and `government-of-canada` (`canada.ca`)
- [x] Include the short aliases `td` and `cra` as requested; leave a note in the plan to review them later
- [x] Confirm `canada.ca` appears only under the government group, not delivery
- [x] Delete `allowed_domains.json`; run `grep -rn allowed_domains` to confirm only docs still mention it

### 3. Rewrite `category_extractor.py` (commit 2)
- [x] Remove the prototype: duplicate `normalize`/`tokenize`/`extract_url`, `setup_nltk_data()`, `SEED_MESSAGES`, `SAMPLE_TEXT`, the `scripts.json_loader` import and the `__main__` block
- [x] Constants: `MIN_FUZZY_ALIAS_LEN = 6`, `BRAND_FUZZY_THRESHOLD = 85`, `BRAND_CONFIDENCE = {"url": 1.0, "exact": 0.9, "fuzzy": 0.8}`
- [x] `get_brand_index()` with `functools.lru_cache`, reading `config/brand_variants.json` via a path relative to the module
- [x] Validate on load: every brand has `slug`, `name`, `domains`; slugs are unique; aliases are strings; raise a clear error otherwise
- [x] Index structure per brand: slug, name, category (group key), alias forms (token sequence and joined string), domain set; plus a `registered_domain -> slug` lookup
- [x] Build alias forms by passing aliases and the brand name through the real `preprocessing.normalizer.normalize` and `tokenize`, so config and message text are normalized identically
- [x] Build a `tldextract.TLDExtract(suffix_list_urls=())` instance once for offline use

### 4. `detect_brand(artifacts) -> dict` (same commit)
- [x] URL pass: for each URL in `extracted_urls` (message order), take its registered domain; collect all brand matches; first one is `url_brand_slug`
- [x] Text pass, exact spaced: slide each alias token sequence over `artifacts["tokens"]`, aliases ordered longest first; ties by earliest position
- [x] Text pass, exact joined: compare each alias's joined form with single tokens (handles `Canada-Post`, `canadapost`)
- [x] Text pass, fuzzy fallback, only when nothing matched exactly and only for aliases with 6+ characters (spaces removed): joined alias vs single tokens via `fuzz.ratio >= BRAND_FUZZY_THRESHOLD`, and spaced alias vs n-grams via `fuzzy_match(..., threshold=BRAND_FUZZY_THRESHOLD)`
- [x] Resolution: URL brand wins; else text brand; else none. Set `brand_slug`, `category`, `text_brand_slug`, `url_brand_slug`, `brand_match_type`, `brand_confidence`
- [x] No input mutation; return a dict of the new fields; no brand returns `None`/`"unknown"`/`None`/`0.0`

### 5. Wire into Phase 0 (commit 3)
- [x] In `extract()`, call `detect_brand` on the built bundle and merge the result over the placeholders
- [x] Confirm no circular import (`category_extractor` must not import `extractor`)
- [x] In `main.py`, add a FastAPI lifespan handler that calls `get_brand_index()` so bad config fails at startup

### 6. Tests
- [x] Rewrite `test_category_extractor.py`: one test per success criterion (exact, only-`Canada`, URL, URL priority, joined form, fuzzy `canadap0st`, short alias not fuzzy, lookalike domain, no brand, longest-alias tie, earliest-in-text tie, multiple URLs, subdomain `tracking.purolator.com`)
- [x] Loader tests: cached (same object on second call), validation errors for missing field and duplicate slug, no import-time side effects
- [x] New `test_normalizer.py` with the 5 prototype tests that pass on the real normalizer (accents, empty string, lowercase, punctuation, homoglyph)
- [x] Extend `test_extractor.py`: new keys present, brand fields filled for a message naming a brand, placeholders preserved for a brand-less message
- [x] Confirm the `fuzzy_match` tests in `test_tokenizer.py` still pass (default stays 80)

### 7. Docs (commit 4)
- [x] `.docs/issues.md`: fix #19 (slug, data source, "scan tokens", amended criteria), #21 and #61 (`allowed_domains.json` wording), #17 (default 80, not 85), #22 (read `text_brand_slug`)
- [x] Remove `allowed_domains.json` from `prd.md`, `overview.md`, `architecture.md`, `source-tree.md`, `coding-standards.md`
- [x] Also fixed (found stale, not in original scope): `rule_engine.md`'s Brand Extraction algorithm + Resolution confidence tiers + URL Checker allowlist wording; `artifacts{}` key lists in `architecture.md`/`prd.md`/`overview.md` (missing `text_brand_slug`/`url_brand_slug`/`brand_match_type`/`brand_confidence`); flagged the 0.8 confidence collision between brand-fuzzy and #20's future keyword-density tier
- [x] Mark #19 done in `.docs/issues.md` and tick its criteria

### 8. Cleanup and validation
- [x] `ruff check backend` and `ruff format --check backend --exclude backend/venv --exclude backend/alembic/versions` are clean
- [x] Full `pytest` passes from the repo root and from `backend/` (94 tests)
- [x] `python -c "from app.core.rules.category_extractor import get_brand_index; get_brand_index()"` runs without network access (verified with socket creation blocked entirely)
- [x] Run `/code-reviewer` before the final commit and record the result in `review.md` — 3 findings, all resolved (2 real alias false-positives fixed, 1 normalizer whitespace gap fixed by user decision)
- [ ] Commit messages use the Title / Why / How / Tags format, no co-author line$$
