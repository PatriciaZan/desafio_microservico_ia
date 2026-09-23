from src.models.ingestion import IngestionResult, IngestionError
from src.models.response import Response
from src.services.clean_response import clean_response
from src.services.remove_duplicates import remove_duplicates

def clean_responses(
    records: list[dict],
) -> IngestionResult:

    responses: list[Response] = []
    errors: list[IngestionError] = []

    for record in records:
        response, error = clean_response(record)
        if error:
            errors.append(error)
            continue
        responses.append(response)

    responses, duplicates = remove_duplicates(responses)

    return IngestionResult(
        total_received=len(records),
        total_accepted=len(responses),
        total_duplicates=duplicates,
        total_rejected=len(errors),
        responses=responses,
        errors=errors,
    )

'''
# versão simplificada v1
def clean_responses(
    records: list[dict],
) -> list[Response]:

    cleaned_responses: list[Response] = []

    for record in records:
        response = clean_response(record)
        if response is None:
            continue

        cleaned_responses.append(response)
    return remove_duplicates(cleaned_responses)

'''