from app.core.preprocessing.tokenizer import _ngrams, get_ngrams, tokenize


# --- tokenize ---


def test_tokenize_basic():
    assert tokenize("Your package is ready") == ["your", "package", "is", "ready"]


def test_tokenize_empty_string():
    assert tokenize("") == []


def test_tokenize_whitespace_only():
    assert tokenize("   ") == []


def test_tokenize_strips_punctuation():
    assert tokenize("Hello, world!") == ["hello", "world"]


def test_tokenize_extra_whitespace():
    assert tokenize("item1  item2") == ["item1", "item2"]


def test_tokenize_alphanumeric_mixed():
    assert tokenize("order #1234 ready") == ["order", "1234", "ready"]


def test_tokenize_underscore_split():
    assert tokenize("your_order") == ["your", "order"]


# --- ngrams ---


def test_ngrams_bigrams():
    assert _ngrams(["a", "b", "c"], 2) == ["a b", "b c"]


def test_ngrams_trigrams():
    assert _ngrams(["a", "b", "c"], 3) == ["a b c"]


def test_ngrams_fewer_tokens_than_n():
    assert _ngrams(["a"], 2) == []


def test_ngrams_empty_tokens():
    assert _ngrams([], 2) == []


def test_ngrams_exact_n():
    assert _ngrams(["a", "b"], 2) == ["a b"]


def test_ngrams_zero_n():
    assert _ngrams(["a", "b", "c"], 0) == []


# --- get_ngrams ---


def test_get_ngrams_combined():
    assert get_ngrams(["a", "b", "c"]) == ["a b", "b c", "a b c"]


def test_get_ngrams_empty():
    assert get_ngrams([]) == []


def test_get_ngrams_single_token():
    assert get_ngrams(["a"]) == []


def test_get_ngrams_two_tokens():
    assert get_ngrams(["a", "b"]) == ["a b"]


def test_get_ngrams_four_tokens():
    assert get_ngrams(["a", "b", "c", "d"]) == ["a b", "b c", "c d", "a b c", "b c d"]
