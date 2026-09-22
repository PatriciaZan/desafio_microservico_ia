from src.models.response import Response


def validate_response(response: Response):
    if not response.pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    if not response.resposta_texto.strip():
        raise ValueError("A resposta não pode estar vazia.")