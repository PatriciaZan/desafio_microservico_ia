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
    # Faz a porcentagem de respostas que citam a marca
    share_of_voice = (
        len(responses_with_brand) / total_responses * 100
        if total_responses
        else 0
    )

    #Calcular sentimento médio para a marca
    sentimentos = [
        response.response.sentimento
        for response in responses_with_brand
        if response.response.sentimento is not None
    ]

    sentimento_info = {}
    if sentimentos:
        # Contar por tipo
        sentimento_info["positivo"] = sentimentos.count("positivo")
        sentimento_info["neutro"] = sentimentos.count("neutro")
        sentimento_info["negativo"] = sentimentos.count("negativo")
        sentimento_info["total_com_sentimento"] = len(sentimentos)
        sentimento_info["percentual_positivo"] = round(sentimento_info["positivo"] / len(sentimentos) * 100, 2)

    by_platform = {}

    for response in responses:
        platform = response.response.plataforma

        by_platform.setdefault(
            platform,
            {
                "total_responses": 0,
                "responses_with_brand": 0,
                "share_of_voice": 0,
                "sentimento": {},
            },
        )

        by_platform[platform]["total_responses"] += 1

        has_brand = any(
            mention.brand.lower() == brand_normalized
            for mention in response.mentions
        )

        if has_brand:
            by_platform[platform]["responses_with_brand"] += 1
            # Contar sentimento por plataforma
            if response.response.sentimento:
                plat_sentimentos = by_platform[platform]["sentimento"]
                plat_sentimentos[response.response.sentimento] = (
                        plat_sentimentos.get(response.response.sentimento, 0) + 1
                )

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
        "sentimento": sentimento_info,
        "by_platform": by_platform,
    }