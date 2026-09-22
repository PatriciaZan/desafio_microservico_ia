from src.models.analyzed_response import AnalyzedResponse


def calculate_share_of_voice(
    responses: list[AnalyzedResponse],
    brand: str,
) -> dict:
    brand_normalized = brand.strip().lower()

    total_responses = len(responses)

    responses_with_brand = [
        response
        for response in responses
        if any(
            mention.brand.lower() == brand_normalized
            for mention in response.mentions
        )
    ]

    total_mentions = sum(
        1
        for response in responses
        for mention in response.mentions
        if mention.brand.lower() == brand_normalized
    )

    share_of_voice = (
        len(responses_with_brand) / total_responses * 100
        if total_responses
        else 0
    )

    by_platform = {}

    for response in responses:
        platform = response.response.plataforma

        by_platform.setdefault(
            platform,
            {
                "total_responses": 0,
                "responses_with_brand": 0,
                "share_of_voice": 0,
            },
        )

        by_platform[platform]["total_responses"] += 1

        has_brand = any(
            mention.brand.lower() == brand_normalized
            for mention in response.mentions
        )

        if has_brand:
            by_platform[platform]["responses_with_brand"] += 1

    for platform, data in by_platform.items():
        data["share_of_voice"] = (
            data["responses_with_brand"]
            / data["total_responses"]
            * 100
        )

    return {
        "brand": brand,
        "total_responses": total_responses,
        "responses_with_brand": len(responses_with_brand),
        "total_mentions": total_mentions,
        "share_of_voice": round(share_of_voice, 2),
        "by_platform": by_platform,
    }

def calculate_citation_strength(
    response: AnalyzedResponse,
) -> int:
    return len(response.mentions)

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