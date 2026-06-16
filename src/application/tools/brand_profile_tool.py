from typing import Dict, Any, Type
from pydantic import BaseModel, Field
from .base_tool import BrandTool
from ..services.brand_profile_service import BrandProfileService

class BrandProfileToolSchema(BaseModel):
    pass # No explicit args needed, takes from state

class BrandProfileTool(BrandTool):
    name = "generate_brand_profile"
    description = """
    Dependency:
    - Requires: website_content
    - Produces: brand_profile (structured summary, mission, positioning)
    - Used by: discover_competitors, generate_creator_guidelines, build_final_toolkit
    
    Rule: DO NOT use if brand_profile is already Present. Use for HR, General, or Marketing overviews of the company.
        """
    args_schema = BrandProfileToolSchema

    def __init__(self, service: BrandProfileService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        content = state.get("website_content")
        if not content:
            return {"tool_message": "Error: website_content is missing. Please use crawl_website tool first."}
            
        print("[*] Tool executing: Extracting Brand Profile using LLM ...")
        profile = self.service.generate_profile(content)
        
        return {
            "brand_profile": profile,
            "tool_message": "Successfully generated BrandProfile and saved to memory. You can now proceed to competitor discovery or creator guidelines."
        }
