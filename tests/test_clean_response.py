import pytest
from src.services.clean_response import clean_response

@pytest.fixture
def valid_data():
    return {
        "id": "1",
        "pergunta": "  Qual   é a melhor marca? ",
        "plataforma": " chatgpt ",
        "modelo": "gpt-5",
        "resposta_texto": "  A Acme é uma ótima marca.  ",
        "data_hora": "22/09/2026",
        "sentimento": None,
    }


def test_clean_response_success(valid_data):
    response, error = clean_response(valid_data)

    assert error is None
    assert response.id == "1"
    assert response.pergunta == "Qual é a melhor marca?"
    assert response.plataforma == "ChatGPT"
    assert response.modelo == "gpt-5"
    assert response.resposta_texto == "A Acme é uma ótima marca."
    assert response.data_hora == "2026-09-22T00:00:00"
    assert response.sentimento is None


def test_clean_response_empty_response(valid_data):
    valid_data["resposta_texto"] = "   "
    response, error = clean_response(valid_data)

    assert response is None
    assert error is not None
    assert error.record_id == "1"
    assert error.reason == "empty_response"


def test_clean_response_missing_field(valid_data):
    del valid_data["plataforma"]
    response, error = clean_response(valid_data)

    assert response is None
    assert error is not None
    assert error.reason == "invalid_data"


def test_clean_response_invalid_date(valid_data):
    valid_data["data_hora"] = "invalid_datetime"
    response, error = clean_response(valid_data)

    assert response is None
    assert error is not None
    assert error.reason == "invalid_datetime"
