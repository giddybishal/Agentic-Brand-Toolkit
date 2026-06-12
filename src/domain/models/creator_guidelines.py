from typing import List
from pydantic import BaseModel

class CreatorGuidelines(BaseModel):
    tone_of_voice: str = ""
    dos: List[str] = []
    donts: List[str] = []
    content_suggestions: List[str] = []
