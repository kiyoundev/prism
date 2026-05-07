import re
import unicodedata

from app.constants import CONFUSABLES, ZERO_WIDTH_CHARS
from unidecode import unidecode

_ZERO_WIDTH_RE = re.compile(f"[{''.join(ZERO_WIDTH_CHARS)}]")

# 1. Lowercase conversion
# 2. Punctuation stripping
# 3. Unicode NFKD normalization (`unicodedata.normalize('NFKD', text)`) — reduces accented chars to base form (e.g., `é` → `e`)
# 4. Homoglyph flattening (`unidecode`) — transliterates Cyrillic/mathematical substitutes to ASCII equivalents
# 5. Zero-width character removal (`​`, `‌`, `‍`, `﻿`, etc.) — used by scammers to break keyword matching


def normalize(text: str) -> str:
    # lowercase conversion
    text = text.lower()

    # strip punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # unicode NFKD normalization
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    # confusable homoglyph substitution (visual match before phonetic transliteration)
    text = "".join(CONFUSABLES.get(c, c) for c in text)

    # homoglyph flattening
    text = unidecode(text)

    # zero-width character removal
    text = _ZERO_WIDTH_RE.sub("", text)

    return text
