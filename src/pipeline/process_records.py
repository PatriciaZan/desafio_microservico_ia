from src.models.response import Response
from src.services.clean_response import clean_response
from src.services.remove_duplicates import remove_duplicates

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