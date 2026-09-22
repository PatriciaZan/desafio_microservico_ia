# analysis

from src.models.analyzed_response import AnalyzedResponse
from src.models.response import Response

from src.services.mentions import detect_mentions

# Analiza uma resposta apenas
def analyze_response(
    response: Response,
) -> AnalyzedResponse:

    mentions = detect_mentions(response.resposta_texto)

    return AnalyzedResponse(
        response=response,
        mentions=mentions,
    )


# analiza tudo
def analyze_responses(
    responses: list[Response],
) -> list[AnalyzedResponse]:

    return [
        analyze_response(response)
        for response in responses
    ]