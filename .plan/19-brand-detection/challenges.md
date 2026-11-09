# Issue #19: Challenges & Notes

## Potential Challenges

1. **Fuzzy matching false positives on short aliases** — `puro` vs the common word `pro` scores 86, so a plain threshold would label "pro tip" as Purolator. Mitigation: aliases under 6 characters (spaces removed) are exact-only. Follow-up #19.5 handles digit lookalikes (`Up5`) without fuzziness.
2. **Exact short aliases can still match ordinary tokens** — `td`, `cra` and `ups` match any token spelled exactly that way (for example "TD:" or "ups and downs"). They are included on request and are to be reviewed later. Watch for false `brand_domain_mismatch` signals in #22.
3. **The documented fuzzy threshold of 85 is stale** — #17's own examples score `amaz0n` 83 and `f3dex` 80, and `test_tokenizer.py` asserts `f3dex` matches `FedEx`. Changing `fuzzy_match`'s default to 85 would break existing tests. Brand detection uses its own 85; fix the #17 text to say 80.
4. **Punctuation deletion joins words** — the normalizer removes punctuation with no space, so `Canada-Post`, `Canada.Post` and zero-width-split names become the single token `canadapost` and miss a spaced alias. Mitigation: match each alias in both spaced and joined forms.
5. **`ngrams` is limited to 2–3 words** — aliases such as `united states postal service` (4 words) never appear in it. Mitigation: match on the token list directly.
6. **Prototype tests don't match the real normalizer** — 2 of the 7 prototype tests fail against `preprocessing.normalizer.normalize`: it does not collapse whitespace (`"Pick   up\n10 AM"` stays `"pick   up\n10 am"`, whitespace-only input stays whitespace). Mitigation: port only the 5 that pass; do not change the normalizer in this issue; token-based matching is unaffected by extra whitespace. Decide separately whether the normalizer should collapse whitespace (it would belong to #14 or #49).
7. **NLTK setup removal** — the prototype downloads `wordnet`/`omw-1.4` at import. #20 needs lemmatization, so that setup must return there as a lazy, explicit step, not an import side effect. `backend/data/nltk_data/` stays gitignored.
8. **Circular imports** — `extractor.py` will import from `rules/category_extractor.py`, which imports `tokenizer.py` and the normalizer. It must never import `extractor.py`.
9. **tldextract network access** — by default it can fetch the public-suffix list on first use. Mitigation: `TLDExtract(suffix_list_urls=())` uses the bundled snapshot; test with the network disabled.
10. **Merged config content is hand-written** — banking and government brands need slugs, names, aliases and domains that do not exist elsewhere. Wrong aliases cause false matches, so start with obvious ones and review. Keep slugs hyphenated and unique (validated at load).
11. **`url_checker.py` shares the config structure** — it builds its own slug-to-domains map from `brand_variants.json`. Adding groups must not break its `_build_brand_map`.
12. **#18 behavior must be preserved** — messages with no brand still return `brand_slug=None` and `category="unknown"`; existing `test_extractor.py` assertions must keep passing.

## Key Differences
| Aspect | Current | Target |
|--------|---------|--------|
| `category_extractor.py` | Prototype with duplicate normalizer and import-time side effects | Brand detection only, cached validated loader |
| Brand slug format in docs | `canada_post` | `canada-post` |
| Domain source for brands | `allowed_domains.json` (category-level, no brand) | `domains` inside `brand_variants.json` |
| Brand lookup input | `tokens` and `ngrams` | `tokens` only (any alias length) |
| `artifacts{}` brand fields | `brand_slug`, `category` placeholders | plus `text_brand_slug`, `url_brand_slug`, `brand_match_type`, `brand_confidence` |
| Fuzzy threshold | `fuzzy_match` default 80 (docs say 85) | brand detection 85, `fuzzy_match` default stays 80 |

## Rollback Plan
1. Revert the branch's commits (`git revert` the four commits, newest first); the config migration commit restores `allowed_domains.json`.
2. Run `pytest` and confirm the 74 existing tests pass.
3. Confirm `extract()` returns `brand_slug=None` for a brand-naming message again (placeholders restored).
