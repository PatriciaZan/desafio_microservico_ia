from collections import Counter

from src.models.analyzed_response import AnalyzedResponse
from src.models.ingestion import IngestionResult
from src.models.report import (
    AnalysisResult,
    IngestionSummary,
    MentionSummary,
)


def build_analysis_result(
    ingestion: IngestionResult,
    analyzed: list[AnalyzedResponse],
) -> AnalysisResult:

    brand_counter = Counter()

    for response in analyzed:
        for mention in response.mentions:
            brand_counter[mention.brand] += 1

    total_mentions = sum(brand_counter.values())

    return AnalysisResult(
        ingestion=IngestionSummary(
            received=ingestion.total_received,
            accepted=ingestion.total_accepted,
            duplicates=ingestion.total_duplicates,
            rejected=ingestion.total_rejected,
        ),
        mentions=MentionSummary(
            total=total_mentions,
            by_brand=dict(brand_counter),
        ),
        responses=analyzed,
    )