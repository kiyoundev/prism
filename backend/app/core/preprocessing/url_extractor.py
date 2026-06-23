import re

from app.constants import _TLDS, _ZERO_WIDTH_RE

_TRAILING_PUNCT_RE = re.compile(r"[.,;:!?)\]>]+$")
_PROTOCOL_RE = re.compile(r"https?://[^\s@]+", re.IGNORECASE)
# Requires a known TLD after @ so trailing-@ scam domains (e.g. domain.com@Expires) are not blanked
_EMAIL_RE = re.compile(r"[^\s@]+@[^\s@]+\.(?:" + _TLDS + r")\b", re.IGNORECASE)
_BARE_DOMAIN_RE = re.compile(
    r"(?<!\w@)"  # defense-in-depth: exclude any residual email domains
    r"\b"  # start at a word boundary; skips leading punctuation like .domain.com
    r"\w(?:[\w\-]*\w)?"  # first domain label; Unicode-aware, no trailing hyphen
    r"(?:\.\w(?:[\w\-]*\w)?)*"  # optional subdomain labels
    r"\.(?:" + _TLDS + r")\b"  # whitelisted ASCII TLD
    r"(?:/[^\s@]*)?",  # optional path; stops at whitespace or @
    re.IGNORECASE,
)


def extract_urls(text: str) -> list[str]:
    # blank email addresses so no part of their domain is extracted as a bare URL
    email_blanked = _EMAIL_RE.sub(lambda m: " " * len(m.group()), text)

    protocol_urls = []
    protocol_spans = []

    for match in _PROTOCOL_RE.finditer(email_blanked):
        protocol_urls.append(_TRAILING_PUNCT_RE.sub("", match.group()))
        protocol_spans.append(match.span())

    scrubbed_chars = list(email_blanked)
    for start, end in protocol_spans:
        for index in range(start, end):
            scrubbed_chars[index] = " "

    scrubbed_text = _ZERO_WIDTH_RE.sub("", "".join(scrubbed_chars))
    bare_domain_urls = [
        _TRAILING_PUNCT_RE.sub("", match.group())
        for match in _BARE_DOMAIN_RE.finditer(scrubbed_text)
    ]

    return protocol_urls + bare_domain_urls
