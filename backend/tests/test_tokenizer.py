from app.core.preprocessing.tokenizer import _ngrams, fuzzy_match, get_ngrams, tokenize


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


# --- fuzzy_match ---


def test_fuzzy_match_accent_obfuscation():
    tokens = tokenize("cañada post")
    assert fuzzy_match(tokens, ["Canada Post"]) == ["Canada Post"]


def test_fuzzy_match_digit_substitution():
    tokens = tokenize("amaz0n")
    assert fuzzy_match(tokens, ["Amazon"]) == ["Amazon"]


def test_fuzzy_match_no_match():
    tokens = tokenize("hello world")
    assert fuzzy_match(tokens, ["Canada Post", "Amazon"]) == []


def test_fuzzy_match_exact():
    tokens = tokenize("amazon")
    assert fuzzy_match(tokens, ["Amazon"]) == ["Amazon"]


def test_fuzzy_match_threshold_configurable():
    tokens = tokenize("amazin")
    assert fuzzy_match(tokens, ["Amazon"], threshold=50) == ["Amazon"]
    assert fuzzy_match(tokens, ["Amazon"], threshold=95) == []


def test_fuzzy_match_empty_tokens():
    assert fuzzy_match([], ["Canada Post"]) == []


def test_fuzzy_match_empty_candidates():
    assert fuzzy_match(tokenize("canada post"), []) == []


def test_fuzzy_match_no_duplicates():
    tokens = tokenize("canada post canada post")
    result = fuzzy_match(tokens, ["Canada Post"])
    assert result == ["Canada Post"]


def test_fuzzy_match_unigram_only_checked_for_single_word_candidate():
    # "FedEx" is 1 word — only unigrams should match, not bigrams
    tokens = tokenize("fedex delivery")
    assert fuzzy_match(tokens, ["FedEx"]) == ["FedEx"]


def test_fuzzy_match_realistic_candidates():
    # candidates built the same way the brand extractor will:
    # name field always included, aliases appended if non-empty
    candidates = [
        "Canada Post", "poste canada", "canada post",
        "Purolator", "puro",
        "FedEx",                                     # aliases is [] — name only
        "UPS", "myups", "united parcel service",
        "USPS", "united states postal service", "us postal service",
        "DHL", "dhl express",
    ]
    # obfuscated "canada post" — accent substitution
    assert "canada post" in fuzzy_match(tokenize("cañada post delivery"), candidates)
    # obfuscated "purolator" — transposed letters
    assert "Purolator" in fuzzy_match(tokenize("puroltaor shipment"), candidates)
    # empty-alias brand matched via name field
    assert "FedEx" in fuzzy_match(tokenize("f3dex package"), candidates)
    # unrelated phrase should not match anything
    assert fuzzy_match(tokenize("click here now"), candidates) == []
