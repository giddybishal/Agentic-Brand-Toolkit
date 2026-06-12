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
            guidelines=state.get("creator_guidelines")
        )
        return {"toolkit": toolkit}
