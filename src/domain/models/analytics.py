from pydantic import BaseModel
from typing import List, Dict

class EngagementMetrics(BaseModel):
    brand_name: str
    average_likes: float
    average_comments: float
    average_shares: float
    posting_frequency: str
    content_type_distribution: Dict[str, float]

class GapAnalysis(BaseModel):
    content_gaps: List[str]
    positioning_gaps: List[str]
    branding_gaps: List[str]
    engagement_gaps: List[str]
    opportunity_areas: List[str]

class GrowthStrategy(BaseModel):
    quick_wins: List[str]
    medium_term_improvements: List[str]
    long_term_recommendations: List[str]
    content_ideas: List[str]
    posting_strategy_suggestions: str
