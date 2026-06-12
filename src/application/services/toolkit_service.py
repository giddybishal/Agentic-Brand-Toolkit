from typing import Optional
from ...domain.models.brand_toolkit import BrandToolkit
from ...domain.models.brand_profile import BrandProfile
from ...domain.models.visual_identity import VisualIdentity
from ...domain.models.creator_guidelines import CreatorGuidelines

class ToolkitService:
    def build_toolkit(
        self,
        url: str,
        profile: Optional[BrandProfile],
        visuals: Optional[VisualIdentity],
        guidelines: Optional[CreatorGuidelines]
    ) -> BrandToolkit:
        return BrandToolkit(
            website_url=url,
            brand_profile=profile,
            visual_identity=visuals,
            creator_guidelines=guidelines
        )
