# Issue #19: Review

## AI Review
<!-- Populated by running `/code-reviewer` before the final commit -->
Ran `/code-review medium` against the full branch diff. 3 confirmed findings, all resolved:

| # | File / Line | Finding | Outcome |
|---|---|---|---|
| 1 | `brand_variants.json:48` | Alias `"royal bank"` on RBC exact-matched unrelated text, e.g. `"Royal Bank of Scotland changed their policy"` → `brand_slug="rbc"`. Verified by direct pipeline run. | **Fixed** — alias removed; `"royal bank of canada"` (unambiguous) kept. Re-verified the exact failing input now returns `brand_slug=None`. |
| 2 | `brand_variants.json:60` | Alias `"scotia"` on Scotiabank exact-matched unrelated text, e.g. `"I grew up in Nova Scotia and love it there"` → `brand_slug="scotiabank"`. Verified by direct pipeline run. | **Fixed** — alias removed; `"bank of nova scotia"` (unambiguous) kept. Re-verified the exact failing input now returns `brand_slug=None`. |
| 3 | `test_normalizer.py` / `normalizer.py` | Reviewer (working blind, without this plan's docs) flagged that 2 whitespace-collapsing tests were dropped during the prototype→real-normalizer test migration, and that `normalize()` doesn't collapse whitespace. This was actually a known, deliberate decision (challenges.md #6) — normalizer behavior was explicitly out of #19's scope, deferred to #14/#49, since token-based brand matching is unaffected by extra whitespace either way. | **Fixed anyway, by user decision** — asked the user whether to leave as documented or expand scope to fix now; chose to fix. Added whitespace collapsing to `normalize()`, restored both dropped tests, added whitespace-collapsing as a 6th step in `rule_engine.md`'s Normalization list. Full suite re-verified green after the change. |

Other angles the reviewer checked against concrete inputs and the full test suite (exact/fuzzy tie-break logic, URL-to-registered-domain lookup, `lru_cache` lazy loading, lifespan startup hook, duplicate-slug/domain validation) held up — no further issues found.

Final state: 94/94 tests passing, `ruff check`/`ruff format --check` clean, both newly-added banking aliases that caused false positives removed and re-verified, normalizer whitespace behavior fixed and covered by tests.

---

## Tech Lead Review
<!-- Populated when PR review comments arrive -->

| # | Comment | File / Line | Status |
|---|---------|-------------|--------|
| 1 | _No comments yet_ | — | ⬜ Open |
