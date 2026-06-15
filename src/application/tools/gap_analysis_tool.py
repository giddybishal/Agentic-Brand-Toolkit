from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.strategy_service import StrategyService

class GapAnalysisToolSchema(BaseModel):
    pass

class GapAnalysisTool(BrandTool):
    name = "perform_gap_analysis"
    description = """
    Description:
    Use this tool to perform a competitive gap analysis.
    
    Input:
    BrandProfile, EngagementMetrics, and CompetitorProfiles (must exist in memory).
    
    Output:
    GapAnalysis.
    
    The output is commonly used by:
    - growth strategy tool
    """
    args_schema = GapAnalysisToolSchema

    def __init__(self, service: StrategyService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        brand_profile = state.get("brand_profile")
        metrics = state.get("engagement_metrics")
        competitor_profiles = state.get("competitor_profiles")
        
        if not all([brand_profile, metrics, competitor_profiles]):
            return {"tool_message": "Error: Missing required data (brand_profile, engagement_metrics, or competitor_profiles)."}
            
        print("[*] Tool executing: Performing Competitive Gap Analysis...")
        gap_analysis = self.service.analyze_gaps(brand_profile, metrics, competitor_profiles)
            
        return {
            "gap_analysis": gap_analysis,
            "tool_message": "Successfully performed gap analysis and saved to memory."
        }
