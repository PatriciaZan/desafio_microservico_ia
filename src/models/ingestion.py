from pydantic import BaseModel

from src.models.response import Response


class IngestionError(BaseModel):
    record_id: str | None = None
    reason: str


class IngestionResult(BaseModel):
    total_received: int
    total_processed: int
    total_duplicates: int
    total_rejected: int

    responses: list[Response]

    errors: list[IngestionError] = []