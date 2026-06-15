from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.social_simulation_service import SocialSimulationService

class SocialDatasetNode:
    def __init__(self, service: SocialSimulationService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        brand_profile = state.get("brand_profile")
        competitor_profiles = state.get("competitor_profiles", [])
        
        if not brand_profile:
            raise ValueError("BrandProfile is required for Social Dataset generation.")
            
        print(f"[*] Simulating realistic social media posts...")
        
        print(f"    -> Generating posts for {brand_profile.brand_name}...")
        brand_social_profile = self.service.simulate_social_profile(brand_profile, brand_profile.brand_name)
        
        comp_social_profiles = []
        for comp in competitor_profiles:
            print(f"    -> Generating posts for {comp.company_name}...")
            comp_social = self.service.simulate_social_profile(comp, comp.company_name)
            comp_social_profiles.append(comp_social)
            
        return {
            "brand_social_profile": brand_social_profile,
            "competitor_social_profiles": comp_social_profiles
        }
