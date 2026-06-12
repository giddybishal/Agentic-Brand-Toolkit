from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.creator_guidelines_service import CreatorGuidelinesService

class CreatorGuidelinesNode:
    def __init__(self, service: CreatorGuidelinesService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        profile = state.get("brand_profile")
        if not profile:
            raise ValueError("BrandProfile is required to generate Creator Guidelines.")
            
        print(f"[*] Generating Creator Guidelines using LLM ...")
        guidelines = self.service.generate_guidelines(profile)
        return {"creator_guidelines": guidelines}
