from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.toolkit_service import ToolkitService

class ToolkitBuilderToolSchema(BaseModel):
    pass

class ToolkitBuilderTool(BrandTool):
    name = "build_final_toolkit"
    description = """
    Dependency:
    - Requires: ALL OF THE ABOVE (if MODE 5)
    - Produces: Complete Brand Toolkit JSON
    - Used by: Final response delivery
    
    Rule: ONLY use this tool if the user explicitly requests a "full brand toolkit" or "generate full pipeline". Do NOT use this for partial queries.
        """
    args_schema = ToolkitBuilderToolSchema

    def __init__(self, service: ToolkitService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        print("[*] Tool executing: Assembling final Brand Toolkit ...")
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
        return {
            "toolkit": toolkit,
            "tool_message": "Final BrandToolkit successfully built. You may now stop execution."
        }
