from src.services.mentions import detect_mentions


def test_detect_single_brand():
    result = detect_mentions("Eu gosto da Acme.")

    assert len(result) == 1
    assert result[0].brand == "Acme"
    assert result[0].matched_text == "Acme"


def test_detect_multiple_brands():
    result = detect_mentions("Eu gosto da Acme e também da Zenith.")

    assert len(result) == 2

    brands = [mention.brand for mention in result]

    assert "Acme" in brands
    assert "Zenith" in brands


def test_detect_brand_case_insensitive():
    result = detect_mentions("ACME é uma empresa conhecida.")

    assert len(result) == 1
    assert result[0].brand == "Acme"
    assert result[0].matched_text == "ACME"


def test_detect_brand_alias():
    result = detect_mentions("A Acme Corp possui vários produtos.")

    assert len(result) == 1
    assert result[0].brand == "Acme"
    assert result[0].matched_text == "Acme Corp"


def test_detect_brand_alias_with_punctuation():
    result = detect_mentions("A empresa A.C.M.E. lançou um produto.")

    assert len(result) == 1
    assert result[0].brand == "Acme"
    assert result[0].matched_text == "A.C.M.E."


def test_detect_no_mentions():
    result = detect_mentions("Esta resposta não menciona nenhuma marca.")

    assert result == []


def test_detect_empty_text():
    result = detect_mentions("")

    assert result == []


def test_detect_repeated_brand():
    result = detect_mentions("Acme é boa. Eu gosto da Acme.")

    assert len(result) == 2

    assert result[0].brand == "Acme"
    assert result[1].brand == "Acme"


def test_detect_longest_alias_only_once():
    result = detect_mentions("A Acme Corp lançou um produto.")

    assert len(result) == 1
    assert result[0].brand == "Acme"
    assert result[0].matched_text == "Acme Corp"