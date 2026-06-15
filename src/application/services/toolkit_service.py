from typing import Optional, List
from ...domain.models.brand_toolkit import BrandToolkit
from ...domain.models.brand_profile import BrandProfile
from ...domain.models.visual_identity import VisualIdentity
from ...domain.models.creator_guidelines import CreatorGuidelines
from ...domain.models.competitor import Competitor, CompetitorProfile
from ...domain.models.social_media import SocialMediaProfile
from ...domain.models.analytics import EngagementMetrics, GapAnalysis, GrowthStrategy

class ToolkitService:
    def build_toolkit(
        self,
        url: str,
        profile: Optional[BrandProfile],
        visuals: Optional[VisualIdentity],
        guidelines: Optional[CreatorGuidelines],
        competitors: Optional[List[Competitor]] = None,
        competitor_profiles: Optional[List[CompetitorProfile]] = None,
        brand_social_profile: Optional[SocialMediaProfile] = None,
        competitor_social_profiles: Optional[List[SocialMediaProfile]] = None,
        engagement_metrics: Optional[List[EngagementMetrics]] = None,
        gap_analysis: Optional[GapAnalysis] = None,
        growth_strategy: Optional[GrowthStrategy] = None
    ) -> BrandToolkit:
        return BrandToolkit(
            website_url=url,
            brand_profile=profile,
            visual_identity=visuals,
            creator_guidelines=guidelines,
            competitors=competitors,
            competitor_profiles=competitor_profiles,
            brand_social_profile=brand_social_profile,
            competitor_social_profiles=competitor_social_profiles,
            engagement_metrics=engagement_metrics,
            gap_analysis=gap_analysis,
            growth_strategy=growth_strategy
        )
