import subprocess
import sys
from pathlib import Path

import pytest

from app.core.preprocessing.extractor import extract
from app.core.rules.category_extractor import (
    _load_brands,
    _match_exact_spaced,
    get_brand_index,
)

# --- detect_brand via extract(): one test per success criterion ---


def test_exact_text_match():
    result = extract("Canada Post: parcel held. Pay now.")
    assert result["brand_slug"] == "canada-post"
    assert result["category"] == "delivery"
    assert result["brand_match_type"] == "exact"
    assert result["brand_confidence"] == 0.9


def test_bare_canada_does_not_match():
    result = extract("Your Canada delivery is delayed")
    assert result["brand_slug"] is None


def test_url_match():
    result = extract("Track your parcel at canadapost.ca/abc123")
    assert result["brand_slug"] == "canada-post"
    assert result["brand_match_type"] == "url"
    assert result["brand_confidence"] == 1.0


def test_url_wins_over_text_but_both_are_kept():
    result = extract("Canada Post: parcel held. Track at fedex.com/abc")
    assert result["brand_slug"] == "fedex"
    assert result["brand_match_type"] == "url"
    assert result["text_brand_slug"] == "canada-post"
    assert result["url_brand_slug"] == "fedex"


@pytest.mark.parametrize(
    "text",
    ["Canada-Post: parcel held", "Canada.Post: parcel held", "CanadaPost: parcel held"],
)
def test_space_collapsed_joined_forms(text):
    result = extract(text)
    assert result["brand_slug"] == "canada-post"
    assert result["brand_match_type"] == "exact"


def test_fuzzy_obfuscated_alias():
    result = extract("your canadap0st parcel is held")
    assert result["brand_slug"] == "canada-post"
    assert result["brand_match_type"] == "fuzzy"
    assert result["brand_confidence"] == 0.8


def test_short_alias_not_fuzzy_matched():
    result = extract("pro tip of the day")
    assert result["brand_slug"] is None


def test_lookalike_domain_rejected():
    result = extract("visit canadapost.ca.parcel-track.xyz now")
    assert result["brand_slug"] is None


def test_no_brand_placeholders():
    result = extract("Hello, how are you today?")
    assert result["brand_slug"] is None
    assert result["category"] == "unknown"
    assert result["brand_match_type"] is None
    assert result["brand_confidence"] == 0.0
    assert result["text_brand_slug"] is None
    assert result["url_brand_slug"] is None


def test_multiple_urls_first_match_wins():
    result = extract("see unknown.example.com then canadapost.ca then purolator.com")
    assert result["url_brand_slug"] == "canada-post"
    assert result["brand_slug"] == "canada-post"


def test_subdomain_resolves_to_registered_domain():
    result = extract("Track at tracking.purolator.com/abc")
    assert result["brand_slug"] == "purolator"
    assert result["brand_match_type"] == "url"


def test_longest_alias_wins_tie_break():
    brands = [
        {
            "slug": "short",
            "aliases": [{"tokens": ("parcel", "service"), "joined": "parcelservice"}],
        },
        {
            "slug": "long",
            "aliases": [
                {
                    "tokens": ("united", "parcel", "service"),
                    "joined": "unitedparcelservice",
                }
            ],
        },
    ]
    tokens = ["your", "united", "parcel", "service", "notice"]
    assert _match_exact_spaced(tokens, brands) == "long"


def test_earliest_position_wins_tie_break():
    brands = [
        {
            "slug": "a",
            "aliases": [{"tokens": ("canada", "post"), "joined": "canadapost"}],
        },
        {
            "slug": "b",
            "aliases": [{"tokens": ("super", "mail"), "joined": "supermail"}],
        },
    ]
    tokens = ["canada", "post", "then", "super", "mail"]
    assert _match_exact_spaced(tokens, brands) == "a"


# --- get_brand_index() loader ---


def test_get_brand_index_is_cached():
    assert get_brand_index() is get_brand_index()


def test_load_brands_missing_field_raises():
    with pytest.raises(ValueError):
        _load_brands({"delivery": [{"slug": "x", "name": "X"}]})


def test_load_brands_duplicate_slug_raises():
    with pytest.raises(ValueError):
        _load_brands(
            {
                "delivery": [
                    {"slug": "x", "name": "X", "domains": ["x.com"]},
                    {"slug": "x", "name": "Y", "domains": ["y.com"]},
                ]
            }
        )


def test_no_import_time_side_effects():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import app.core.rules.category_extractor as m\n"
            "assert m.get_brand_index.cache_info().misses == 0, "
            "'index was built at import time'",
        ],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[1],
    )
    assert result.returncode == 0, result.stderr
