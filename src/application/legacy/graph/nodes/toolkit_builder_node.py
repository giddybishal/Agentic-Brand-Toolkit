from typing import Dict, Any
from ....domain.models.graph_state import BrandState

from ...services.toolkit_service import ToolkitService

class ToolkitBuilderNode:
    def __init__(self, service: ToolkitService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        print(f"[*] Assembling final Brand Toolkit ...")
        toolkit = self.service.build_toolkit(
            url=state.get("website_url", ""),
            profile=state.get("brand_profile"),
            visuals=state.get("visual_identity"),
            guidelines=state.get("creator_guidelines"),
            competitors=state.get("competitors"),
            competitor_profiles=state.get("competitor_profiles"),
            brand_social_profile=state.get("brand_social_profile"),
            competitor_social_profiles=state.get("competitor_social_profiles"),
            engagement_metrics=state.get("engagement_metrics"),
            gap_analysis=state.get("gap_analysis"),
            growth_strategy=state.get("growth_strategy")
        )
        return {"toolkit": toolkit}
