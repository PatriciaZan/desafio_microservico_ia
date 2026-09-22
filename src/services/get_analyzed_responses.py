from src.models.ingestion import IngestionResult
from src.models.analyzed_response import AnalyzedResponse
from src.services.analyze_response import analyze_responses
from src.services.cleaning import clean_responses
from src.services.ingestion import load_responses_local


def get_analyzed_responses() -> list[AnalyzedResponse]:
    records = load_responses_local()
    ingestion_result = clean_responses(records)

    return analyze_responses(ingestion_result.responses)

def get_analysis_data() -> tuple[
    IngestionResult,
    list[AnalyzedResponse],
]:
    records = load_responses_local()
    ingestion_result = clean_responses(records)
    analyzed_responses = analyze_responses(ingestion_result.responses)

    return ingestion_result, analyzed_responses