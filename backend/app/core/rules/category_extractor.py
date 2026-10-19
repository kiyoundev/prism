"""
Category extraction pipeline checklist:
- Normalize first
  • Lowercase, strip punctuation, collapse whitespace.
  • Apply Unicode normalization + homoglyph handling (unicodedata.normalize, unidecode, unhomoglyph).
  • Remove accents so variants like “délivery” still match “delivery”.
- Tokenize + optional lemmatize/stem
  • Use a simple tokenizer (spaCy, NLTK/natural, regex splitter).
  • Lemmatization/stemming collapses inflections (“deliveries” → “delivery”).
- Build n-grams / phrase windows
  • Generate 2–5 word windows to catch cues like “return to sender” before single tokens.
- Match and score
  • Compare phrase windows and single tokens against category keyword lists.
  • Weight phrases higher than single tokens (e.g., +1.0 vs +0.5) and log hits as evidence.
- Post-process
  • Choose the highest-scoring category above a threshold; break ties by phrase weight.
  • If nothing clears the bar, fall back to None/"generic".
- Enhancements
  • Optional fuzzy/Levenshtein for short cues (“otp”, “pin”) gated by context.
  • Keep JSON synonyms updated (e.g., “reschedule”, “dispatch” for delivery).
  • Optionally blend in a lightweight classifier (e.g., Naive Bayes) and require agreement for ambiguous cases.
"""

import re
import unicodedata
from unidecode import unidecode
import string
import nltk
from nltk.tokenize import RegexpTokenizer
from typing import List, Dict, Any
import os

from scripts.json_loader import load_json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../../.."))
NLTK_DATA_DIR = os.path.join(PROJECT_ROOT, "backend/data/nltk_data")

URL_PATTERN = re.compile(r"https?://[^\s]+")
SEED_MESSAGES = load_json("backend/data/seed_scams.json")
BRANDS = load_json("backend/app/core/rules/config/brand_variants.json")
SAMPLE_TEXT = SEED_MESSAGES[0]["text"]

nltk.data.path.append(NLTK_DATA_DIR)


def setup_nltk_data():
    nltk.data.path.append(NLTK_DATA_DIR)
    # Download required corpora if missing
    try:
        nltk.data.find("corpora/wordnet.zip")
    except LookupError:
        print(f"Downloading NLTK 'wordnet' to {NLTK_DATA_DIR}...")
        nltk.download("wordnet", download_dir=NLTK_DATA_DIR)
    try:
        nltk.data.find("corpora/omw-1.4.zip")
    except LookupError:
        print(f"Downloading NLTK 'omw-1.4' to {NLTK_DATA_DIR}...")
        nltk.download("omw-1.4", download_dir=NLTK_DATA_DIR)


setup_nltk_data()


def extract_url(text: str) -> str:
    urls: list[str] = []

    def _protect(match: re.Match[str]) -> str:
        urls.append(match.group(0))
        return f"URLTOKEN{len(urls) - 1}"

    url_protected = URL_PATTERN.sub(_protect, text)
    print(url_protected)


def normalize(text: str) -> str:
    """
    Normalize text for category matching:
    - Lowercase
    - Remove extra whitespace
    - Handle Unicode normalization
    - Remove homoglyphs before ASCII encoding
    - Encode to ASCII, ignoring non-ASCII characters
    - Preserve URLs by masking them temporarily
    """
    urls: list[str] = []

    def _protect(match: re.Match[str]) -> str:
        urls.append(match.group(0))
        return f"URLTOKEN{len(urls) - 1}"

    def _restore(match: re.Match[str]) -> str:
        return urls[int(match.group(1))]

    # Lowercase
    lowered = text.lower()
    url_protected = URL_PATTERN.sub(_protect, lowered)
    # Remove punctuation
    punct_stripped = re.sub(rf"[{re.escape(string.punctuation)}]", " ", url_protected)
    # Remove extra whitespace
    whitespace_cleaned = re.sub(r"\s+", " ", punct_stripped).strip()
    # Unicode normalization
    normalized = unicodedata.normalize("NFKD", whitespace_cleaned)
    # Remove homoglyphs before ASCII encoding
    homoglyph_flat = unidecode(normalized)
    # Encode to ASCII, ignoring non-ASCII characters
    encoded = homoglyph_flat.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"URLTOKEN(\d+)", _restore, encoded)


def tokenize(text: str) -> list[str]:
    word_tokenizer = RegexpTokenizer(r"[a-z0-9]+")
    return word_tokenizer.tokenize(text)


def build_brand_index(
    brands_json: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, Dict[str, Any]]:
    """
    Returns:
      brand_index: {
        slug: {
          'name': 'Purolator',
          'aliases': ['purolator', 'puro', ...],  # normalized strings
          'alias_token_seqs': [['purolator'], ['puro'], ['united','parcel','service'], ...]
        },
        ...
      }
    """
    brand_index = {}
    for entry in brands_json.get("delivery", []):
        slug = entry["slug"]
        aliases = entry.get("aliases", [])
        name = entry["name"]

        all_aliases = set(normalize(alias) for alias in aliases)
        all_aliases.add(normalize(name))

        alias_token_seqs = []

        for alias in all_aliases:
            tokens = tokenize(alias)
            alias_token_seqs.append(tokens)

        brand_index[slug] = {
            "name": name,
            "aliases": list(all_aliases),
            "alias_token_seqs": alias_token_seqs,
        }
    return brand_index


# def extract_category(text: str) -> str:
# lemmatizer = WordNetLemmatizer()
# normalized_text = normalize(text)
# tokens = tokenize(normalized_text)
# token_set = set(lemmatizer.lemmatize(token) for token in tokens)
# print(tokens)
# print(token_set)


if __name__ == "__main__":
    # setup_nltk_data()
    extract_url(SAMPLE_TEXT)
