from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.creator_guidelines_service import CreatorGuidelinesService

class CreatorGuidelinesToolSchema(BaseModel):
    pass

class CreatorGuidelinesTool(BrandTool):
    name = "generate_creator_guidelines"
    description = """
    Description:
    Use this tool to generate content creator guidelines for the brand.
    
    Input:
    BrandProfile (must exist in memory).
    
    Output:
    CreatorGuidelines.
    
    The output is commonly used by:
    - toolkit builder
    """
    args_schema = CreatorGuidelinesToolSchema

    def __init__(self, service: CreatorGuidelinesService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        profile = state.get("brand_profile")
        if not profile:
            return {"tool_message": "Error: BrandProfile is missing. Generate brand profile first."}
            
        print("[*] Tool executing: Generating Creator Guidelines using LLM ...")
        guidelines = self.service.generate_guidelines(profile)
        
        return {
            "creator_guidelines": guidelines,
            "tool_message": "Successfully generated creator guidelines and saved to memory."
        }
