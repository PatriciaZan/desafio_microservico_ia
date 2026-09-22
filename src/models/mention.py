
from pydantic import BaseModel

class Mention(BaseModel):
    brand: str
    matched_text: str