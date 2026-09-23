from src.services.clean_text import clean_text

def test_clean_text_removes_extra_spaces():
    result = clean_text("  Olá    mundo   ")
    assert result == "Olá mundo"


def test_clean_text_returns_empty_string_for_none():
    result = clean_text(None)
    assert result == ""


def test_clean_text_returns_empty_string_for_empty_string():
    result = clean_text("")
    assert result == ""


def test_clean_text_handles_only_spaces():
    result = clean_text("     ")
    assert result == ""