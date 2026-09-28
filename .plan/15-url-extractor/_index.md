# #15: url_extractor.py — extract URLs before normalization

## PR / Branch
- **Branch:** `feature/15-url-extractor`
- **PR Title:** `main | feature - 15 - url_extractor.py`

## Task Status

| Step | Status | File |
|------|--------|------|
| Context & Planning | ✅ Done | [context.md](context.md) |
| Implementation | ⬜ Not started | [implementation.md](implementation.md) |
| Challenges | ⬜ Not started | [challenges.md](challenges.md) |
| Review | ⬜ Not started | [review.md](review.md) |

## Success Criteria

- [ ] Extracts standard `http://` and `https://` URLs from plain text
- [ ] Extracts bare domains without protocol (e.g., `bit.ly/abc123`, `manage-account-detail.com`)
- [ ] Handles multiple URLs in a single message
- [ ] Preserves the original form of each URL (no lowercasing or stripping)
- [ ] Returns an empty list for messages with no URLs
- [ ] Does not extract email addresses as URLs

## Estimated Effort
- Implementation: **0.5 hours**
- Testing: **0.5 hours**
- **Total: ~1 hour**
