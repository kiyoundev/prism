from app.core.preprocessing.normalizer import normalize


def test_normalize_strips_accents():
    assert normalize("délivery") == "delivery"


def test_normalize_empty_string():
    assert normalize("") == ""


def test_normalize_whitespace():
    assert normalize("Pick   up\n10 AM") == "pick up 10 am"


def test_normalize_only_whitespace():
    assert normalize("   \n\t  ") == ""


def test_normalize_lowercase():
    assert normalize("HELLO WORLD") == "hello world"


def test_normalize_punctuation():
    assert normalize("Hello, world!") == "hello world"


def test_normalize_homoglyphs():
    assert normalize("Dёlivery") == "delivery"
