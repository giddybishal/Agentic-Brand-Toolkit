from pydantic import BaseModel
from typing import Optional, List
from .visual_identity import VisualIdentity
from .brand_profile import BrandProfile
from .creator_guidelines import CreatorGuidelines
from .competitor import Competitor, CompetitorProfile
from .social_media import SocialMediaProfile
from .analytics import EngagementMetrics, GapAnalysis, GrowthStrategy

class BrandToolkit(BaseModel):
    website_url: str
    brand_profile: Optional[BrandProfile] = None
    visual_identity: Optional[VisualIdentity] = None
    creator_guidelines: Optional[CreatorGuidelines] = None
    competitors: Optional[List[Competitor]] = None
    competitor_profiles: Optional[List[CompetitorProfile]] = None
    brand_social_profile: Optional[SocialMediaProfile] = None
    competitor_social_profiles: Optional[List[SocialMediaProfile]] = None
    engagement_metrics: Optional[List[EngagementMetrics]] = None
    gap_analysis: Optional[GapAnalysis] = None
    growth_strategy: Optional[GrowthStrategy] = None
