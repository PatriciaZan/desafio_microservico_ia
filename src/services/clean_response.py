from pydantic import ValidationError

from src.models.response import Response

from src.services.normalize_datetime import normalize_datetime
from src.services.clean_text import clean_text
from src.services.normalize_platform import normalize_platform


def clean_response(
    data: dict,
) -> Response | None:

    data = data.copy()

    # Normalização de texto
    data["pergunta"] = clean_text(data.get("pergunta"))

    data["resposta_texto"] = clean_text(data.get("resposta_texto"))

    # Resposta vazia não pode ser analisada
    if not data["resposta_texto"]:
        return None

    # Normalização da plataforma
    data["plataforma"] = normalize_platform(data["plataforma"])

    # Normalização da data
    data["data_hora"] = normalize_datetime( data.get("data_hora"))

    try:
        return Response.model_validate(data)
    except ValidationError as error:
        print(
            f"Registro inválido "
            f"{data.get('id')}: {error}"
        )
        return None