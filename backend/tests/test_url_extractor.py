
from app.core.preprocessing.url_extractor import extract_urls


# --- Protocol URLs ---


def test_protocol_https():
    assert extract_urls("Click here: https://example.com/path") == ["https://example.com/path"]


def test_protocol_http():
    assert extract_urls("Visit http://example.com") == ["http://example.com"]


def test_protocol_case_insensitive():
    assert extract_urls("Go to HTTPS://EXAMPLE.COM") == ["HTTPS://EXAMPLE.COM"]


# --- Bare domains ---


def test_bare_domain_with_path():
    assert extract_urls("Check bit.ly/abc123 for details") == ["bit.ly/abc123"]


def test_bare_domain_no_path():
    assert extract_urls("Go to manage-account-detail.com") == ["manage-account-detail.com"]


# --- Multiple URLs ---


def test_multiple_urls():
    result = extract_urls("Visit https://evil.com and also bit.ly/abc")
    assert result == ["https://evil.com", "bit.ly/abc"]


def test_multiple_bare_domains():
    result = extract_urls("See bit.ly/x and also example.com")
    assert "bit.ly/x" in result
    assert "example.com" in result


# --- Preservation of original form ---


def test_preserves_casing():
    result = extract_urls("https://Example.COM/Path")
    assert result == ["https://Example.COM/Path"]


def test_preserves_percent_encoding():
    result = extract_urls("https://example.com/path%20here")
    assert result == ["https://example.com/path%20here"]


# --- Empty / no URL ---


def test_empty_string():
    assert extract_urls("") == []


def test_no_urls():
    assert extract_urls("Your package has been delivered successfully.") == []


def test_version_string_ignored():
    assert extract_urls("App version 2.0 released") == []


# --- Email exclusion ---


def test_email_excluded():
    assert extract_urls("Contact user@ontario.ca for help") == []


def test_email_with_subdomain_excluded():
    # Email pre-blanking ensures even parent domains of subdomain emails are excluded
    assert extract_urls("Send to support@mail.example.com") == []


# --- Edge cases ---


def test_trailing_punctuation_stripped_protocol():
    assert extract_urls("Visit https://example.com.") == ["https://example.com"]


def test_trailing_punctuation_stripped_bare():
    assert extract_urls("Go to example.com!") == ["example.com"]


def test_no_double_match():
    # Protocol URL must not appear in both passes
    result = extract_urls("https://bit.ly/abc")
    assert result.count("https://bit.ly/abc") == 1
    assert "bit.ly/abc" not in result


def test_leading_dot():
    # Real corpus pattern: ".domain.com" — leading dot must be skipped
    assert extract_urls("See .domain.com for details") == ["domain.com"]


def test_trailing_at_scam():
    # Real corpus: "See .crasecurecadeposit.com@Expires 29-01-25"
    result = extract_urls("Your Hst-Ref#76577 for $435 is now ready. See .crasecurecadeposit.com@Expires 29-01-25.")
    assert result == ["crasecurecadeposit.com"]


# --- Attack vectors ---


def test_punycode_url():
    # Attack #1: IDN/punycode — ASCII, caught by protocol pass
    assert extract_urls("https://xn--pple-43d.com") == ["https://xn--pple-43d.com"]


def test_unicode_protocol_url():
    # Attack #2: raw Unicode in protocol URL (Cyrillic а U+0430)
    assert extract_urls("https://аpple.com") == ["https://аpple.com"]


def test_unicode_bare_domain():
    # Attack #3: raw Unicode bare domain (Cyrillic а U+0430)
    assert extract_urls("аpple.com") == ["аpple.com"]


def test_zws_inside_bare_domain():
    # Attack #4: zero-width space mid-label breaks naive \w boundary
    assert extract_urls("bit.l​y/abc") == ["bit.ly/abc"]


def test_zws_before_protocol_url():
    # ZWS immediately before protocol URL must not suppress extraction
    result = extract_urls("​https://example.com")
    assert "https://example.com" in result


# --- Corpus spot-checks ---


def test_corpus_protocol_vip_tld():
    # From known-scams: https://purolator.etcydh.vip/ca
    assert extract_urls("Your parcel: https://purolator.etcydh.vip/ca") == [
        "https://purolator.etcydh.vip/ca"
    ]


def test_corpus_protocol_top_tld():
    # From known-scams: https://canada.postscanadacuy.top/ca
    assert extract_urls("https://canada.postscanadacuy.top/ca") == [
        "https://canada.postscanadacuy.top/ca"
    ]


def test_corpus_bare_domain_manage_account():
    # From known-scams: manage-account-detail.com (embedded in homoglyph text)
    assert extract_urls("Please update your details at manage-account-detail.com") == [
        "manage-account-detail.com"
    ]
