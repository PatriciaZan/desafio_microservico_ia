from src.models.response import Response

# r003
# tenho de verificar a possibilidade de ids iguais, mas conteúdos diferentes

def remove_duplicates(
    responses: list[Response],
) -> tuple[list[Response], int]:

    seen_ids: set[str] = set()
    unique_responses: list[Response] = []

    duplicates = 0

    for response in responses:

        if response.id in seen_ids:
            duplicates += 1
            continue

        seen_ids.add(response.id)
        unique_responses.append(response)

    return unique_responses, duplicates