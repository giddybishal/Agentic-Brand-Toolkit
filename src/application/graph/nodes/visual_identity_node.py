from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.visual_identity_service import VisualIdentityService

class VisualIdentityNode:
    def __init__(self, service: VisualIdentityService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        url = state.get("website_url", "")
        print(f"[*] Extracting Visual Identity (colors, logos, typography) from {url} ...")
        identity = self.service.extract_visual_identity(url)
        return {"visual_identity": identity}
