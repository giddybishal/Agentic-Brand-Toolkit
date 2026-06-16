from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.analytics_service import EngagementAnalyticsService

class EngagementAnalyticsToolSchema(BaseModel):
    pass

class EngagementAnalyticsTool(BrandTool):
    name = "compute_engagement_analytics"
    description = """
    Dependency:
    - Requires: brand_social_profile, competitor_social_profiles
    - Produces: engagement_metrics
    - Used by: perform_gap_analysis
    
    Rule: DO NOT use if engagement_metrics is already Present. Use only for social analytics.
        """
    args_schema = EngagementAnalyticsToolSchema

    def __init__(self, service: EngagementAnalyticsService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        brand_social = state.get("brand_social_profile")
        comp_socials = state.get("competitor_social_profiles", [])
        
        if not brand_social:
            return {"tool_message": "Error: brand_social_profile is missing. Generate social dataset first."}
            
        print("[*] Tool executing: Computing Engagement Analytics...")
        metrics = []
        metrics.append(self.service.compute_metrics(brand_social))
        
        for comp in comp_socials:
            metrics.append(self.service.compute_metrics(comp))
            
        return {
            "engagement_metrics": metrics,
            "tool_message": "Successfully computed engagement metrics for all social profiles."
        }
