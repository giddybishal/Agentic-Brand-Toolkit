from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.competitor_service import CompetitorDiscoveryService

class CompetitorIntelligenceToolSchema(BaseModel):
    pass

class CompetitorIntelligenceTool(BrandTool):
    name = "generate_competitor_intelligence"
    description = """
    Dependency:
    - Requires: competitors list
    - Produces: competitor_profiles (detailed competitor data)
    - Used by: perform_gap_analysis, build_final_toolkit
    
    Rule: DO NOT use if competitor_profiles is already Present. Use only when deep competitor analysis is requested.
        """
    args_schema = CompetitorIntelligenceToolSchema

    def __init__(self, service: CompetitorDiscoveryService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        competitors = state.get("competitors")
        if not competitors:
            return {"tool_message": "Error: competitors missing. Run competitor discovery first."}
            
        print(f"[*] Tool executing: Extracting Intelligence Profiles for {len(competitors)} competitors...")
        profiles = []
        for c in competitors:
            print(f"    -> Analyzing {c.name}...")
            profile = self.service.generate_competitor_profile(c)
            profiles.append(profile)
            
        return {
            "competitor_profiles": profiles,
            "tool_message": f"Successfully generated {len(profiles)} competitor intelligence profiles and saved to memory."
        }
