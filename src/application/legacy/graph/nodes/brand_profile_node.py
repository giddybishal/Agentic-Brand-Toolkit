from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.brand_profile_service import BrandProfileService

class BrandProfileNode:
    def __init__(self, service: BrandProfileService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        content = state.get("website_content", "")
        print(f"[*] Extracting Brand Profile using LLM ...")
        profile = self.service.generate_profile(content)
        return {"brand_profile": profile}
