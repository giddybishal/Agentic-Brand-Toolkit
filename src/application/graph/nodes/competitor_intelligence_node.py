from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.competitor_service import CompetitorDiscoveryService

class CompetitorIntelligenceNode:
    def __init__(self, service: CompetitorDiscoveryService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        competitors = state.get("competitors")
        if not competitors:
            raise ValueError("Competitors are required for Competitor Intelligence.")
            
        print(f"[*] Extracting Intelligence Profiles for {len(competitors)} competitors...")
        profiles = []
        for c in competitors:
            print(f"    -> Analyzing {c.name}...")
            profile = self.service.generate_competitor_profile(c)
            profiles.append(profile)
            
        return {"competitor_profiles": profiles}
