from src.models.analyzed_response import AnalyzedResponse
from src.metrics.metric_citation_strength import calculate_citation_strength

# Uma citação é mais forte quando:

#1. Tem mais marcas - mais contexto competitivo
#2. Tem sentimento positivo - a marca é falada bem
#3. A pergunta é relevante - sobre a própria marca/mercado dela (não sobre IA trends genérico)

# Assim minha justificativa é:
# Marca com sentimento positivo é mais valiosa (você quer saber quando falam BEM)
# Múltiplas menções importam, mais citadas com um sentimento positivo = mais peso

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
            "mentions": len(response.mentions),
            "sentimento": response.response.sentimento,
            "citation_strength": calculate_citation_strength(
                response
            ),
        }
        for response in ranked[:limit]
    ]