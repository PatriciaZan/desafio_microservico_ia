from pydantic import BaseModel

from src.models.analyzed_response import AnalyzedResponse

# contrato claro para API.
class IngestionSummary(BaseModel):
    received: int
    accepted: int
    duplicates: int
    rejected: int


class MentionSummary(BaseModel):
    total: int
    by_brand: dict[str, int]


class AnalysisResult(BaseModel):
    ingestion: IngestionSummary
    mentions: MentionSummary
    responses: list[AnalyzedResponse]