from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.competitor_service import CompetitorDiscoveryService

class CompetitorDiscoveryToolSchema(BaseModel):
    pass

class CompetitorDiscoveryTool(BrandTool):
    name = "discover_competitors"
    description = """
    Description:
    Use this tool to discover the brand's top competitors based on its profile.
    
    Input:
    BrandProfile (must exist in memory).
    
    Output:
    List of Competitors.
    
    The output is commonly used by:
    - competitor intelligence tool
    """
    args_schema = CompetitorDiscoveryToolSchema

    def __init__(self, service: CompetitorDiscoveryService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        profile = state.get("brand_profile")
        if not profile:
            return {"tool_message": "Error: brand_profile is missing. Generate it first."}
            
        print("[*] Tool executing: Discovering top competitors...")
        competitors = self.service.discover_competitors(profile)
        
        return {
            "competitors": competitors,
            "tool_message": f"Successfully discovered {len(competitors)} competitors and saved to memory. You can now use competitor intelligence tool."
        }
