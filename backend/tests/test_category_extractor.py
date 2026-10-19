import pytest
from app.core.rules.category_extractor import normalize

@pytest.mark.normalize
def test_normalize_strips_accents():
    assert normalize("délivery") == "delivery"
    
@pytest.mark.normalize
def test_normalize_whitespace():
    assert normalize("Pick   up\n10 AM") == "pick up 10 am"

@pytest.mark.normalize
def test_normalize_empty_string():
    assert normalize("") == ""

@pytest.mark.normalize
def test_normalize_only_whitespace():
    assert normalize("   \n\t  ") == ""
    
@pytest.mark.normalize
def test_normalize_lowercase():
    assert normalize("HELLO WORLD") == "hello world"

@pytest.mark.normalize
def test_normalize_punctuation():
    assert normalize("Hello, world!") == "hello world"

@pytest.mark.normalize
def test_normalize_homoglyphs():
    assert normalize("Dёlivery") == "delivery"

