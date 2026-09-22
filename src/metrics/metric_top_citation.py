from src.models.analyzed_response import AnalyzedResponse
from src.metrics.metric_citation_strength import calculate_citation_strength


def get_top_citations(
    responses: list[AnalyzedResponse],
    limit: int,
) -> list[dict]:

    ranked = sorted(
        responses,
        key=calculate_citation_strength,
        reverse=True,
    )

    return [
        {
            "id": response.response.id,
            "platform": response.response.plataforma,
            "question": response.response.pergunta,
            "response": response.response.resposta_texto,
            "brands": [
                mention.brand
                for mention in response.mentions
            ],
            "citation_strength": calculate_citation_strength(
                response
            ),
        }
        for response in ranked[:limit]
    ]