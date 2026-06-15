from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.competitor_service import CompetitorDiscoveryService

class CompetitorIntelligenceToolSchema(BaseModel):
    pass

class CompetitorIntelligenceTool(BrandTool):
    name = "generate_competitor_intelligence"
    description = """
    Description:
    Use this tool to extract detailed intelligence profiles for discovered competitors.
    
    Input:
    List of Competitors (must exist in memory).
    
    Output:
    List of CompetitorProfiles.
    
    The output is commonly used by:
    - social dataset tool
    - gap analysis
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
