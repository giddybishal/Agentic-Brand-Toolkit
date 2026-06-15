from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.competitor_service import CompetitorDiscoveryService

class CompetitorDiscoveryNode:
    def __init__(self, service: CompetitorDiscoveryService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        profile = state.get("brand_profile")
        if not profile:
            raise ValueError("BrandProfile is required for Competitor Discovery.")
            
        print(f"[*] Discovering top competitors...")
        competitors = self.service.discover_competitors(profile)
        for c in competitors:
            print(f"    - {c.name} ({c.relevance_score}/100)")
            
        return {"competitors": competitors}
