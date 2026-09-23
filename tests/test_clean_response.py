VALID_RESPONSE = {
    "id": "1",
    "pergunta": "  Qual   é a melhor marca? ",
    "plataforma": " chatgpt ",
    "modelo": "gpt-5",
    "resposta_texto": "  A Acme é uma ótima marca.  ",
    "data_hora": "22/09/2026",
    "sentimento": None,
}

from src.services.clean_response import clean_response


def test_clean_response_returns_valid_response():
    data = {
        "id": "1",
        "pergunta": "  Qual   é a melhor marca? ",
        "plataforma": " chatgpt ",
        "modelo": "gpt-5",
        "resposta_texto": "  A Acme é uma ótima marca.  ",
        "data_hora": "22/09/2026",
        "sentimento": None,
    }

    response, error = clean_response(data)

    assert error is None
    assert response is not None

    assert response.id == "1"
    assert response.pergunta == "Qual é a melhor marca?"
    assert response.plataforma == "ChatGPT"
    assert response.modelo == "gpt-5"
    assert response.resposta_texto == "A Acme é uma ótima marca."
    assert response.data_hora == "2026-09-22T00:00:00"
    assert response.sentimento is None

def test_clean_response_rejects_empty_response():
    data = {
        "id": "2",
        "pergunta": "Qual é a melhor marca?",
        "plataforma": "chatgpt",
        "modelo": "gpt-5",
        "resposta_texto": "   ",
        "data_hora": "22/09/2026",
        "sentimento": None,
    }

    response, error = clean_response(data)

    assert response is None

    assert error is not None
    assert error.record_id == "2"
    assert error.reason == "empty_response"

def test_clean_response_rejects_invalid_data():
    data = {
        "id": "3",
        "pergunta": "Qual é a melhor marca?",
        # plataforma está faltando
        "modelo": "gpt-5",
        "resposta_texto": "A Acme é ótima.",
        "data_hora": "22/09/2026",
        "sentimento": None,
    }

    response, error = clean_response(data)

    assert response is None
    assert error is not None
    assert error.record_id == "3"