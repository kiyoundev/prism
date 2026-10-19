import re

from rapidfuzz import fuzz


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _ngrams(tokens: list[str], n: int) -> list[str]:
    if n < 1 or len(tokens) < n:
        return []
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def get_ngrams(tokens: list[str]) -> list[str]:
    return _ngrams(tokens, 2) + _ngrams(tokens, 3)


def fuzzy_match(
    tokens: list[str], candidates: list[str], threshold: int = 80
) -> list[str]:
    phrases_by_len: dict[int, list[str]] = {}
    for token in tokens:
        phrases_by_len.setdefault(1, []).append(token)
    for phrase in get_ngrams(tokens):
        n = len(phrase.split())
        phrases_by_len.setdefault(n, []).append(phrase)

    matched = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        n = len(candidate.split())
        for phrase in phrases_by_len.get(n, []):
            if fuzz.ratio(phrase, candidate.lower()) >= threshold:
                matched.append(candidate)
                seen.add(candidate)
                break
    return matched
