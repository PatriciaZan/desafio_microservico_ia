from pydantic import BaseModel

from src.models.mention import Mention
from src.models.response import Response


class AnalyzedResponse(BaseModel):
    response: Response
    mentions: list[Mention]