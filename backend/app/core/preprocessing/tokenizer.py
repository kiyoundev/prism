import re


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _ngrams(tokens: list[str], n: int) -> list[str]:
    if n < 1 or len(tokens) < n:
        return []
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def get_ngrams(tokens: list[str]) -> list[str]:
    return _ngrams(tokens, 2) + _ngrams(tokens, 3)
