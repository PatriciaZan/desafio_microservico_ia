from pydantic import ValidationError

from src.models.ingestion import IngestionError
from src.models.response import Response

from src.services.normalize_datetime import normalize_datetime
from src.services.clean_text import clean_text
from src.services.normalize_platform import normalize_platform


def clean_response(
    data: dict,
) -> tuple[Response | None, IngestionError | None]: # por que retornou None

    data = data.copy()
    record_id = data.get("id")

    # Normalização de texto
    data["pergunta"] = clean_text(data.get("pergunta"))

    data["resposta_texto"] = clean_text(data.get("resposta_texto"))

    # Resposta vazia não pode ser analisada
    if not data["resposta_texto"]:
        return (
            None,
            IngestionError(
                record_id=record_id,
                reason="empty_response",
            ),
        )
    try:
        # Normalização da plataforma
        data["plataforma"] = normalize_platform(data["plataforma"])

        # Normalização da data
        data["data_hora"] = normalize_datetime( data.get("data_hora"))

        response = Response.model_validate(data)
        return response, None


    except KeyError:
        return (
            None,
            IngestionError(
                record_id=record_id,
                reason="invalid_data",
            ),
        )

    except ValueError as error:
        return (
            None,
            IngestionError(
                record_id=record_id,
                reason=str(error),
            ),
        )

    except ValidationError:
        return (
            None,
            IngestionError(
                record_id=record_id,
                reason="invalid_data",

            ),

        )
