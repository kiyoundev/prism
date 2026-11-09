from app.core.preprocessing.normalizer import normalize
from app.core.preprocessing.tokenizer import get_ngrams, tokenize
from app.core.preprocessing.url_extractor import extract_urls
from app.core.rules.category_extractor import detect_brand


def extract(text: str) -> dict:
    if not text or not text.strip():
        raise ValueError("Input text must not be empty or whitespace-only")

    extracted_urls = extract_urls(text)

    clean_text = text
    for url in extracted_urls:
        clean_text = clean_text.replace(url, " ")

    normalized_text = normalize(clean_text)
    tokens = tokenize(normalized_text)
    ngrams = get_ngrams(tokens)

    artifacts = {
        "extracted_urls": extracted_urls,
        "normalized_text": normalized_text,
        "tokens": tokens,
        "ngrams": ngrams,
    }
    artifacts.update(detect_brand(artifacts))

    return artifacts
