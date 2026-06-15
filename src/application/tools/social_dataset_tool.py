from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.social_simulation_service import SocialSimulationService

class SocialDatasetToolSchema(BaseModel):
    pass

class SocialDatasetTool(BrandTool):
    name = "generate_social_dataset"
    description = """
    Description:
    Use this tool to simulate realistic social media posts for the brand and its competitors.
    
    Input:
    BrandProfile and CompetitorProfiles (must exist in memory).
    
    Output:
    BrandSocialProfile and List of CompetitorSocialProfiles.
    
    The output is commonly used by:
    - engagement analytics tool
    """
    args_schema = SocialDatasetToolSchema

    def __init__(self, service: SocialSimulationService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        brand_profile = state.get("brand_profile")
        competitor_profiles = state.get("competitor_profiles", [])
        
        if not brand_profile:
            return {"tool_message": "Error: brand_profile is missing."}
            
        print("[*] Tool executing: Simulating realistic social media posts...")
        brand_social_profile = self.service.simulate_social_profile(brand_profile, brand_profile.brand_name)
        
        comp_social_profiles = []
        for comp in competitor_profiles:
            comp_social = self.service.simulate_social_profile(comp, comp.company_name)
            comp_social_profiles.append(comp_social)
            
        return {
            "brand_social_profile": brand_social_profile,
            "competitor_social_profiles": comp_social_profiles,
            "tool_message": "Successfully generated social media datasets for brand and competitors."
        }
