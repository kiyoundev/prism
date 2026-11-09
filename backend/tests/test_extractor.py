import pytest

from app.core.preprocessing.extractor import extract


# --- output shape ---


def test_extract_returns_all_keys():
    result = extract("Your package is ready")
    assert set(result.keys()) == {
        "extracted_urls",
        "normalized_text",
        "tokens",
        "ngrams",
        "brand_slug",
        "category",
        "text_brand_slug",
        "url_brand_slug",
        "brand_match_type",
        "brand_confidence",
    }


def test_extract_placeholders():
    result = extract("Your package is ready")
    assert result["brand_slug"] is None
    assert result["category"] == "unknown"
    assert result["text_brand_slug"] is None
    assert result["url_brand_slug"] is None
    assert result["brand_match_type"] is None
    assert result["brand_confidence"] == 0.0


def test_extract_brand_fields_filled_for_known_brand():
    result = extract("Canada Post: parcel held")
    assert result["brand_slug"] == "canada-post"
    assert result["category"] == "delivery"
    assert result["brand_match_type"] == "exact"
    assert result["brand_confidence"] == 0.9


# --- url extraction ---


def test_extract_urls_before_normalization():
    result = extract("Track at fedex.com/track now")
    assert "fedex.com/track" in result["extracted_urls"]


def test_extract_urls_not_in_tokens():
    result = extract("Track at fedex.com/track now")
    assert not any("fedex" in t and "com" in t for t in result["tokens"])


def test_extract_no_urls():
    result = extract("Your package is ready")
    assert result["extracted_urls"] == []


# --- normalization ---


def test_extract_normalized_text():
    result = extract("Your Package Is READY!")
    assert result["normalized_text"] == "your package is ready"


def test_extract_tokens_from_normalized_text():
    result = extract("Your package is ready")
    assert result["tokens"] == ["your", "package", "is", "ready"]


# --- ngrams ---


def test_extract_ngrams_present():
    result = extract("Your package is ready")
    assert "your package" in result["ngrams"]
    assert "package is ready" in result["ngrams"]


# --- url stripped from tokens and ngrams ---


def test_extract_url_stripped_from_normalized_text():
    result = extract("Track at fedex.com/track now")
    assert "fedexcomtrack" not in result["normalized_text"]


def test_extract_url_stripped_from_ngrams():
    result = extract("Track at fedex.com/track now")
    assert not any("fedexcomtrack" in ng for ng in result["ngrams"])


# --- error handling ---


def test_extract_raises_on_empty_string():
    with pytest.raises(ValueError):
        extract("")


def test_extract_raises_on_whitespace_only():
    with pytest.raises(ValueError):
        extract("   ")
