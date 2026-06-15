from pydantic import BaseModel
from typing import List

class Competitor(BaseModel):
    name: str
    industry: str
    reasoning: str
    relevance_score: int

class CompetitorProfile(BaseModel):
    company_name: str
    positioning_summary: str
    strengths: List[str]
    target_audience: str
    content_strategy_summary: str

class CompetitorList(BaseModel):
    competitors: List[Competitor]
