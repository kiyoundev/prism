import re
import unicodedata

from app.constants import _CONFUSABLES, _ZERO_WIDTH_RE
from unidecode import unidecode

# 1. Lowercase conversion
# 2. Punctuation stripping
# 3. Unicode NFKD normalization (`unicodedata.normalize('NFKD', text)`) — reduces accented chars to base form (e.g., `é` → `e`)
# 4. Homoglyph flattening (`unidecode`) — transliterates Cyrillic/mathematical substitutes to ASCII equivalents
# 5. Zero-width character removal (`​`, `‌`, `‍`, `﻿`, etc.) — used by scammers to break keyword matching
# 6. Whitespace collapsing — runs of whitespace (including from URL-stripping and multi-line text) become a single space


def normalize(text: str) -> str:
    # lowercase conversion
    text = text.lower()

    # strip punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # unicode NFKD normalization
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    # confusable homoglyph substitution (visual match before phonetic transliteration)
    text = "".join(_CONFUSABLES.get(c, c) for c in text)

    # homoglyph flattening
    text = unidecode(text)

    # zero-width character removal
    text = _ZERO_WIDTH_RE.sub("", text)

    # whitespace collapsing
    text = re.sub(r"\s+", " ", text).strip()

    return text
