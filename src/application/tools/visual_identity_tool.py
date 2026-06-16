from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.visual_identity_service import VisualIdentityService

class VisualIdentityToolSchema(BaseModel):
    pass

class VisualIdentityTool(BrandTool):
    name = "extract_visual_identity"
    description = """
    Dependency:
    - Requires: website_url and website_content
    - Produces: visual_identity (colors, fonts, logos)
    - Used by: build_final_toolkit
    
    Rule: DO NOT use if visual_identity is already Present. Use ONLY if the user specifically asks for colors, logos, or visual branding (e.g. Designer mode).
        """
    args_schema = VisualIdentityToolSchema

    def __init__(self, service: VisualIdentityService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        url = state.get("website_url")
        if not url:
            return {"tool_message": "Error: website_url is missing."}
            
        print(f"[*] Tool executing: Extracting Visual Identity from {url} ...")
        identity = self.service.extract_visual_identity(url)
        
        return {
            "visual_identity": identity,
            "tool_message": "Successfully extracted VisualIdentity and saved to memory."
        }
