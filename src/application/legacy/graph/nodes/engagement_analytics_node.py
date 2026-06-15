from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.analytics_service import EngagementAnalyticsService

class EngagementAnalyticsNode:
    def __init__(self, service: EngagementAnalyticsService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        brand_social = state.get("brand_social_profile")
        comp_socials = state.get("competitor_social_profiles", [])
        
        if not brand_social:
            raise ValueError("Brand social profile is required for analytics.")
            
        print(f"[*] Computing Engagement Analytics...")
        
        metrics = []
        brand_metrics = self.service.compute_metrics(brand_social)
        metrics.append(brand_metrics)
        
        for comp in comp_socials:
            metrics.append(self.service.compute_metrics(comp))
            
        return {"engagement_metrics": metrics}
