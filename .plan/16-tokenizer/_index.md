# Issue #16: tokenizer.py — word tokens + bi/tri-grams

## PR / Branch
- **Branch:** `feature/16-tokenizer`
- **PR Title:** `main | feature - 16 - tokenizer`

## Task Status
| Step | Status | File |
|------|--------|------|
| Context & Planning | ✅ Done | [context.md](context.md) |
| Implementation | ✅ Done | [implementation.md](implementation.md) |
| Review | ✅ Done | [review.md](review.md) |

## Success Criteria
- [ ] `tokenize("Your package is ready")` returns `["your", "package", "is", "ready"]`
- [ ] `tokenize` strips punctuation and handles extra whitespace
- [ ] `ngrams(["a", "b", "c"], 2)` returns `["a b", "b c"]`
- [ ] `get_ngrams(tokens)` returns the union of bi-grams and tri-grams
- [ ] Empty string input returns empty lists without raising

## Estimated Effort
- Implementation: **0.5 hours**
- Testing: **0.5 hours**
- **Total: 1 hour**

## Git Commit Message
```
Add: tokenizer with word tokens and bi/tri-grams

Why:
Phase 0 pipeline needs token lists and n-gram phrases for brand
detection and TF-IDF feature extraction downstream.

How:
- Add 'tokenize()' — alphanumeric-only split via re.findall
- Add '_ngrams()' — sliding window phrase builder (private)
- Add 'get_ngrams()' — public API returning bi+tri-grams combined
- Add 18 tests covering edge cases: empty input, n=0 guard,
  underscore boundary, whitespace, punctuation stripping

Tags:
preprocessing, tokenization, ngrams, phase-0, issue-16
```