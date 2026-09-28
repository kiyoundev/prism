# #15: Implementation

## Steps

### 1. Module-level regex constants

- [ ] Define `_TRAILING_PUNCT_RE = re.compile(r'[.,;:!?)\]>]+$')` — strips trailing punctuation from protocol URL matches
- [ ] Define `_PROTOCOL_RE = re.compile(r'https?://[^\s@]+', re.IGNORECASE)` — stops at whitespace and `@`
- [ ] Define `_TLDS` string covering all TLDs observed in `known-scams.md` plus common shortener and scam TLDs:
  ```
  com|ca|net|org|io|gov|edu|co|us|uk|ly|me|biz|info|app|dev
  |xyz|vip|cc|tv|gl|eu|fr|de|au|nz|ru|jp|mobi|online|shop
  |site|store|top|tech|news|pro|live|club|blog|link|click
  ```
- [ ] Import `ZERO_WIDTH_CHARS` from `app.constants` — already defined there; use it to strip ZWS from `scrubbed_text` before the bare domain pass (attack #4). No new constant needed.
- [ ] Define `_BARE_DOMAIN_RE` with:
  - `(?<!\w@)` — negative lookbehind excluding email domains (e.g., `user@ontario.ca`); `\w` is Unicode-aware so homoglyph emails (e.g., `ϲοηѕʋμεг@ontario.ca`) are also excluded
  - `\b` — word boundary; handles leading-dot case (`See .domain.com`)
  - Label pattern `\w(?:[\w\-]*\w)?` — **`\w` not `[a-zA-Z0-9]`** so Cyrillic/Greek homoglyph labels match (attacks #2, #3)
  - `\.(?:TLD)\b` — ASCII TLD whitelist; `\b` prevents `company` matching on TLD `com`; TLD stays ASCII since all real TLDs are ASCII even for IDN domains
  - `(?:/[^\s@]*)?` — optional path; stops at whitespace or `@` (handles trailing-`@` scam pattern)

### 2. Helper and main function

- [ ] Implement `_strip_trailing_punct(url: str) -> str` using `_TRAILING_PUNCT_RE`
- [ ] Implement `extract_urls(text: str) -> list[str]`:
  1. Iterate `_PROTOCOL_RE.finditer(text)` → strip trailing punct → collect results + spans
  2. Build `scrubbed_text` by blanking protocol URL character spans (replace with spaces)
  3. Strip ZWS chars from `scrubbed_text` — preserves original form of already-captured protocol URLs since their spans are blanked (attack #4)
  4. Iterate `_BARE_DOMAIN_RE.finditer(scrubbed_text)` → strip trailing punct → collect results
  5. Return combined list (protocol URLs first, then bare domains)

### 3. Tests — `backend/tests/test_url_extractor.py`

- [ ] `test_protocol_https` — standard `https://` URL extracted
- [ ] `test_protocol_http` — standard `http://` URL extracted
- [ ] `test_bare_domain_with_path` — `bit.ly/abc123` extracted
- [ ] `test_bare_domain_no_path` — `manage-account-detail.com` extracted
- [ ] `test_multiple_urls` — message with both a protocol URL and a bare domain returns both
- [ ] `test_preserves_original_form` — casing and percent-encoding unchanged
- [ ] `test_empty_string` — returns `[]`
- [ ] `test_no_urls` — plain text with no URLs returns `[]`
- [ ] `test_email_excluded` — `user@ontario.ca` → `ontario.ca` not in result
- [ ] `test_trailing_at_scam` — `See .crasecurecadeposit.com@Expires 29-01-25` → `['crasecurecadeposit.com']`
- [ ] `test_leading_dot` — `See .domain.com` → `['domain.com']`
- [ ] `test_no_double_match` — `https://bit.ly/abc` not returned twice (once from each pass)
- [ ] `test_trailing_punctuation_stripped` — `https://example.com.` → `https://example.com`
- [ ] `test_version_string_ignored` — `version 2.0` → `[]`
- [ ] `test_unicode_bare_domain` — `аpple.com` (Cyrillic `а`) → `['аpple.com']` (attack #3)
- [ ] `test_unicode_protocol_url` — `https://аpple.com` (Cyrillic `а`) → `['https://аpple.com']` (attack #2)
- [ ] `test_punycode_url` — `https://xn--pple-43d.com` → `['https://xn--pple-43d.com']` (attack #1)
- [ ] `test_zws_inside_bare_domain` — `bit.l​y/abc` (ZWS mid-label) → `['bit.ly/abc']` (attack #4)
- [ ] `test_zws_before_protocol_url` — ZWS immediately before `https://` URL → URL still extracted
- [ ] Corpus spot-checks: representative entries from `data/known-scams/known-scams.md` (both protocol and bare domain cases)

### 4. Cleanup

- [ ] Run `ruff check backend/app/core/preprocessing/url_extractor.py` and fix any errors
- [ ] Confirm no type-hint warnings (`mypy` or IDE diagnostics)
