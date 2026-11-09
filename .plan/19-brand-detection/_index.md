# Issue #19: category_extractor.py — brand detection

## PR / Branch
- **Branch:** `feature/19-brand-detection`
- **PR Title:** `main | feature - 19 - brand detection`

## Task Status
| Step | Status | File |
|------|--------|------|
| Context & Planning | ✅ Done | [context.md](context.md) |
| Implementation | ⬜ Not started | [implementation.md](implementation.md) |
| Challenges | ⬜ Not started | [challenges.md](challenges.md) |
| Review | ⬜ Not started | [review.md](review.md) |

## Success Criteria
Derived from the issue's acceptance criteria, amended by the design decisions in `context.md`.

- [ ] Text containing `"Canada Post"` resolves to `brand_slug="canada-post"`, `category="delivery"`, `brand_match_type="exact"`, `brand_confidence=0.9` (slug is hyphenated, matching `brand_variants.json`)
- [ ] Text containing only `"Canada"` does not match `canada-post`
- [ ] A link on `canadapost.ca` resolves to `canada-post` regardless of text, with `brand_match_type="url"` and `brand_confidence=1.0`
- [ ] A URL brand match wins over a text brand match, and both `text_brand_slug` and `url_brand_slug` are kept in `artifacts{}`
- [ ] Space-collapsed forms match exactly: `Canada-Post`, `Canada.Post`, `CanadaPost` all resolve to `canada-post`
- [ ] Obfuscated long aliases match fuzzily at threshold 85: `canadap0st` resolves to `canada-post`, `brand_match_type="fuzzy"`, `brand_confidence=0.8`
- [ ] Aliases shorter than 6 characters (spaces removed) are never matched fuzzily: `pro` does not match `puro`
- [ ] A lookalike link such as `canadapost.ca.parcel-track.xyz` does not match Canada Post (registered domain is `parcel-track.xyz`)
- [ ] `brand_variants.json` is read once through a cached loader, validated at load, and also loaded at FastAPI startup; no import-time side effects and no `scripts` import
- [ ] `detect_brand(artifacts)` is a pure function; `extract()` merges its fields into `artifacts{}`
- [ ] With no brand detected, `brand_slug=None`, `category="unknown"`, `brand_match_type=None`, `brand_confidence=0.0`
- [ ] `allowed_domains.json` is deleted and its content lives in `brand_variants.json` (banking and government groups added; `canada.ca` under a government brand, not delivery)
- [ ] All existing tests still pass, new tests cover every criterion above, `ruff check` and `ruff format --check` are clean

## Estimated Effort
- Implementation: **3 hours** (issue estimated ~2h; scope grew with fuzzy matching, config migration, wiring and doc fixes)
- Testing: **1.5 hours**
- **Total: 4.5 hours**
- Follow-up #19.5 (lookalike-digit folding for short aliases) is separate: ~1h
