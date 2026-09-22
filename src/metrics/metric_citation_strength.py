
from src.models.analyzed_response import AnalyzedResponse

def calculate_citation_strength(
        response: AnalyzedResponse,
) -> float:
    mention_count = len(response.mentions)

    sentiment_weight = 0
    if response.response.sentimento == "positivo":
        sentiment_weight = 1
    elif response.response.sentimento == "neutro":
        sentiment_weight = 0
    elif response.response.sentimento == "negativo":
        sentiment_weight = -0.5

    return mention_count + sentiment_weight