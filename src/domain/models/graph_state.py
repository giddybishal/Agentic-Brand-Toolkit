from typing import TypedDict, Optional, Any, List
from .visual_identity import VisualIdentity
from .brand_profile import BrandProfile
from .creator_guidelines import CreatorGuidelines
from .brand_toolkit import BrandToolkit
from .competitor import Competitor, CompetitorProfile
from .social_media import SocialMediaProfile
from .analytics import EngagementMetrics, GapAnalysis, GrowthStrategy

class BrandState(TypedDict, total=False):
    website_url: str
    website_content: Optional[str]
    visual_identity: Optional[VisualIdentity]
    brand_profile: Optional[BrandProfile]
    creator_guidelines: Optional[CreatorGuidelines]
    competitors: Optional[List[Competitor]]
    competitor_profiles: Optional[List[CompetitorProfile]]
    brand_social_profile: Optional[SocialMediaProfile]
    competitor_social_profiles: Optional[List[SocialMediaProfile]]
    engagement_metrics: Optional[List[EngagementMetrics]]
    gap_analysis: Optional[GapAnalysis]
    growth_strategy: Optional[GrowthStrategy]
    toolkit: Optional[BrandToolkit]
