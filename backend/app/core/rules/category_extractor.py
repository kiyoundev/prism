import json
from functools import lru_cache
from pathlib import Path

import tldextract
from rapidfuzz import fuzz

from app.core.preprocessing.normalizer import normalize
from app.core.preprocessing.tokenizer import fuzzy_match, tokenize

CONFIG_PATH = Path(__file__).parent / "config" / "brand_variants.json"
REQUIRED_FIELDS = ("slug", "name", "domains")

MIN_FUZZY_ALIAS_LEN = 6
BRAND_FUZZY_THRESHOLD = 85
BRAND_CONFIDENCE = {"url": 1.0, "exact": 0.9, "fuzzy": 0.8}


def _alias_forms(raw: str) -> dict:
    tokens = tuple(tokenize(normalize(raw)))
    return {"tokens": tokens, "joined": "".join(tokens)}


def _load_brands(data: dict) -> list[dict]:
    brands = []
    seen_slugs: set[str] = set()

    for category, entries in data.items():
        for entry in entries:
            missing = [field for field in REQUIRED_FIELDS if field not in entry]
            if missing:
                raise ValueError(
                    f"brand_variants.json: entry in '{category}' missing {missing}: {entry}"
                )

            slug = entry["slug"]
            if slug in seen_slugs:
                raise ValueError(f"brand_variants.json: duplicate slug '{slug}'")
            seen_slugs.add(slug)

            aliases_raw = entry.get("aliases", [])
            if not all(isinstance(alias, str) for alias in aliases_raw):
                raise ValueError(
                    f"brand_variants.json: '{slug}' aliases must be strings"
                )

            alias_sources = {*aliases_raw, entry["name"]}
            aliases = [
                form
                for form in (_alias_forms(alias) for alias in alias_sources)
                if form["tokens"]
            ]

            brands.append(
                {
                    "slug": slug,
                    "name": entry["name"],
                    "category": category,
                    "aliases": aliases,
                    "domains": set(entry["domains"]),
                }
            )

    return brands


def _domain_lookup(
    brands: list[dict], extract_domain: tldextract.TLDExtract
) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for brand in brands:
        for domain in brand["domains"]:
            registered = extract_domain(domain).registered_domain
            if registered in lookup:
                raise ValueError(
                    f"brand_variants.json: domain '{domain}' claimed by both "
                    f"'{lookup[registered]}' and '{brand['slug']}'"
                )
            lookup[registered] = brand["slug"]
    return lookup


@lru_cache(maxsize=1)
def get_brand_index() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    extract_domain = tldextract.TLDExtract(suffix_list_urls=())
    brands = _load_brands(data)
    domain_to_slug = _domain_lookup(brands, extract_domain)

    return {
        "brands": brands,
        "domain_to_slug": domain_to_slug,
        "extract_domain": extract_domain,
    }


def _match_url_brand(extracted_urls: list[str], index: dict) -> str | None:
    for url in extracted_urls:
        try:
            registered = index["extract_domain"](url).registered_domain
        except Exception:
            continue
        slug = index["domain_to_slug"].get(registered)
        if slug:
            return slug
    return None


def _match_exact_spaced(tokens: list[str], brands: list[dict]) -> str | None:
    matches = []  # (alias_len, start, slug)
    for brand in brands:
        for alias in brand["aliases"]:
            alias_tokens = alias["tokens"]
            n = len(alias_tokens)
            if n < 2:
                continue
            for start in range(len(tokens) - n + 1):
                if tuple(tokens[start : start + n]) == alias_tokens:
                    matches.append((n, start, brand["slug"]))

    if not matches:
        return None
    matches.sort(key=lambda m: (-m[0], m[1]))
    return matches[0][2]


def _match_exact_joined(tokens: list[str], brands: list[dict]) -> str | None:
    for token in tokens:
        for brand in brands:
            for alias in brand["aliases"]:
                if alias["joined"] and alias["joined"] == token:
                    return brand["slug"]
    return None


def _fuzzy_alias_candidates(brands: list[dict], min_words: int) -> list[tuple]:
    candidates = []  # (len(joined), alias, slug)
    for brand in brands:
        for alias in brand["aliases"]:
            if len(alias["tokens"]) < min_words:
                continue
            if len(alias["joined"]) >= MIN_FUZZY_ALIAS_LEN:
                candidates.append((len(alias["joined"]), alias, brand["slug"]))
    candidates.sort(key=lambda c: -c[0])
    return candidates


def _match_fuzzy_joined(tokens: list[str], brands: list[dict]) -> str | None:
    for _, alias, slug in _fuzzy_alias_candidates(brands, min_words=1):
        for token in tokens:
            if fuzz.ratio(alias["joined"], token) >= BRAND_FUZZY_THRESHOLD:
                return slug
    return None


def _match_fuzzy_spaced(tokens: list[str], brands: list[dict]) -> str | None:
    candidates = _fuzzy_alias_candidates(brands, min_words=2)
    spaced_to_slug = {" ".join(alias["tokens"]): slug for _, alias, slug in candidates}
    ordered_strings = list(spaced_to_slug.keys())

    matched = fuzzy_match(tokens, ordered_strings, threshold=BRAND_FUZZY_THRESHOLD)
    return spaced_to_slug[matched[0]] if matched else None


def _category_for_slug(slug: str, brands: list[dict]) -> str:
    return next(brand["category"] for brand in brands if brand["slug"] == slug)


def detect_brand(artifacts: dict) -> dict:
    index = get_brand_index()
    brands = index["brands"]
    tokens = artifacts["tokens"]

    url_brand_slug = _match_url_brand(artifacts["extracted_urls"], index)

    exact_slug = _match_exact_spaced(tokens, brands) or _match_exact_joined(
        tokens, brands
    )
    if exact_slug:
        text_brand_slug = exact_slug
        text_match_type = "exact"
    else:
        fuzzy_slug = _match_fuzzy_joined(tokens, brands) or _match_fuzzy_spaced(
            tokens, brands
        )
        text_brand_slug = fuzzy_slug
        text_match_type = "fuzzy" if fuzzy_slug else None

    if url_brand_slug:
        brand_slug = url_brand_slug
        brand_match_type = "url"
    elif text_brand_slug:
        brand_slug = text_brand_slug
        brand_match_type = text_match_type
    else:
        brand_slug = None
        brand_match_type = None

    category = _category_for_slug(brand_slug, brands) if brand_slug else "unknown"

    return {
        "brand_slug": brand_slug,
        "category": category,
        "text_brand_slug": text_brand_slug,
        "url_brand_slug": url_brand_slug,
        "brand_match_type": brand_match_type,
        "brand_confidence": BRAND_CONFIDENCE.get(brand_match_type, 0.0),
    }
