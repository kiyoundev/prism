# Issue #16: Implementation

## Steps

### 1. Write `tokenizer.py`
- [x] `tokenize(text)` — `re.findall(r'[a-z0-9]+', text.lower())` handles lowercase, alphanumeric-only, strips punctuation, collapses whitespace in one pass
- [x] `ngrams(tokens, n)` — sliding window: `[" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]`; return `[]` when `len(tokens) < n`
- [x] `get_ngrams(tokens)` — `ngrams(tokens, 2) + ngrams(tokens, 3)`

### 2. Write `test_tokenizer.py`

Cover all acceptance criteria plus edge cases:

- [x] `tokenize("Your package is ready")` → `["your", "package", "is", "ready"]`
- [x] `tokenize("")` → `[]`
- [x] `tokenize("   ")` → `[]`
- [x] `tokenize("Hello, world!")` → `["hello", "world"]`
- [x] `tokenize("item1  item2")` → `["item1", "item2"]` (extra whitespace collapsed)
- [x] `ngrams(["a", "b", "c"], 2)` → `["a b", "b c"]`
- [x] `ngrams(["a", "b", "c"], 3)` → `["a b c"]`
- [x] `ngrams(["a"], 2)` → `[]` (fewer tokens than n)
- [x] `ngrams([], 2)` → `[]`
- [x] `get_ngrams(["a", "b", "c"])` → `["a b", "b c", "a b c"]`
- [x] `get_ngrams([])` → `[]`
- [x] `get_ngrams(["a"])` → `[]` (single token produces no bigrams or trigrams)
