# #15: Challenges & Notes

## URL Attack Vectors

The table below documents all known URL obfuscation techniques relevant to SMS phishing, their handling status in `extract_urls`, and the responsible fix or downstream owner.

| # | Attack | Example | Pass 1 (Protocol) | Pass 2 (Bare Domain) | Fix / Owner |
|---|--------|---------|:-----------------:|:--------------------:|-------------|
| 1 | **Punycode / IDN** | `https://xn--pple-43d.com` | ✅ ASCII — caught | ✅ ASCII — caught | No action needed |
| 2 | **Raw Unicode protocol URL** | `https://аpple.com` (Cyrillic `а`) | ✅ `[^\s@]+` is not ASCII-restricted | ✅ `\w` label pattern catches it | Use `\w` not `[a-zA-Z0-9]` for label chars (this issue) |
| 3 | **Bare Unicode domain** | `аpple.com` (Cyrillic `а`) | — | ✅ `\w` label pattern catches it | Use `\w` not `[a-zA-Z0-9]` for label chars (this issue) |
| 4 | **ZWS inside domain label** | `bit.l​y/abc` (U+200B mid-label) | ✅ ZWS not `\s` — captured as-is; Phase 1 strips during URL normalization | ❌ ZWS breaks `\w` boundary — domain missed | Strip ZWS from `scrubbed_text` before bare domain pass only (this issue) |
| 5 | **Auth-URL `@` abuse** | `https://google.com@evil.com/phish` | ❌ `[^\s@]+` stops at `@` — `evil.com` never captured | — | Out of scope; rare in corpus; Phase 1 concern |
| 6 | **Bare IP address** | `192.168.1.1/login` | ✅ Protocol IPs (`https://1.2.3.4`) caught | ❌ No TLD — regex never matches | Out of scope; Phase 1 `url_checker.py` already signals `IP_ADDRESS_URL` for protocol IPs |

### ZWS strip strategy (attack #4)

Strip ZWS characters from `scrubbed_text` only — the version used for the bare domain pass. Protocol URL spans are already blanked at that point, so original form of protocol URLs is preserved. The ZWS-embedded protocol URL captured in pass 1 reaches Phase 1 intact, where step 1 of the URL Checker normalizes it.

```python
from app.constants import _ZERO_WIDTH_CHARS

_ZWS_SET = set(_ZERO_WIDTH_CHARS)  # module-level, built once
scrubbed_text = ''.join(c for c in scrubbed_text if c not in _ZWS_SET)
```

### Unicode label pattern (attacks #2 and #3)

Use `\w` (Python 3 `re` is Unicode-aware by default) for domain label characters instead of `[a-zA-Z0-9]`. The ASCII TLD whitelist provides precision — false positives from allowing Unicode labels are bounded by the TLD anchor.

`\w` includes underscore `_`, which is technically invalid in domain labels. Acceptable for MVP — underscores are never observed in the scam corpus.

## Implementation Challenges

1. **TLD whitelist drift** — scammers actively register on new gTLDs not in the list. The static whitelist will miss future TLDs (e.g., `.zip`, `.mov`). Mitigation for MVP: cover all TLDs observed in the known-scams corpus plus a broad set of common gTLDs. Long-term: swap to `tldextract` (already a project dependency in `url_checker.py`) for authoritative PSL-based TLD detection.

2. **`url_checker.py` duplicate `extract_urls`** — `URLChecker.extract_urls` (line 37–40) is protocol-only and stays in place. It is called internally within Phase 1. The Phase 0 `extract_urls` in `url_extractor.py` is the canonical pre-normalization extractor. Do not merge in this issue — flag for cleanup when the pipeline orchestrator is wired up.

3. **Regex backtracking on bare domain pattern** — the subdomain repetition group followed by `\.TLD` creates potential backtracking on pathological inputs. Mitigation: SMS messages are short (<500 chars) so this is low risk for MVP. If needed, impose a timeout via the `regex` library.

## Key Differences

| Aspect | Current (`url_checker.py`) | Target (`url_extractor.py`) |
|--------|---------------------------|------------------------------|
| Scope | Protocol URLs only (`https?://`) | Protocol URLs + bare domains |
| Phase | Phase 1 (post-normalization context) | Phase 0 (raw text, pre-normalization) |
| Email exclusion | None | `(?<!\w@)` lookbehind |
| Trailing `@` scam | Not handled | Stops match at `@` via path pattern |
| TLD filtering | None (accepts any URL) | Whitelist guards against false positives |
