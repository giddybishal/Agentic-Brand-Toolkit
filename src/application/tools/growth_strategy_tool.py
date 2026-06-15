from typing import Dict, Any, Type
from pydantic import BaseModel
from .base_tool import BrandTool
from ..services.strategy_service import StrategyService

class GrowthStrategyToolSchema(BaseModel):
    pass

class GrowthStrategyTool(BrandTool):
    name = "generate_growth_strategy"
    description = """
    Description:
    Use this tool to generate a social growth strategy.
    
    Input:
    BrandProfile, GapAnalysis, EngagementMetrics, and CompetitorProfiles (must exist in memory).
    
    Output:
    GrowthStrategy.
    
    The output is commonly used by:
    - toolkit builder
    """
    args_schema = GrowthStrategyToolSchema

    def __init__(self, service: StrategyService):
        self.service = service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        brand_profile = state.get("brand_profile")
        gap_analysis = state.get("gap_analysis")
        metrics = state.get("engagement_metrics")
        competitor_profiles = state.get("competitor_profiles")
        
        if not all([brand_profile, gap_analysis, metrics, competitor_profiles]):
            return {"tool_message": "Error: Missing data for Growth Strategy. Ensure brand_profile, gap_analysis, engagement_metrics, and competitor_profiles are generated."}
            
        print("[*] Tool executing: Generating Social Growth Strategy...")
        strategy = self.service.generate_growth_strategy(brand_profile, gap_analysis, metrics, competitor_profiles)
            
        return {
            "growth_strategy": strategy,
            "tool_message": "Successfully generated growth strategy and saved to memory."
        }
