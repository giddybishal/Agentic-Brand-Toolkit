from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.strategy_service import StrategyService

class GrowthStrategyNode:
    def __init__(self, service: StrategyService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        brand_profile = state.get("brand_profile")
        gap_analysis = state.get("gap_analysis")
        metrics = state.get("engagement_metrics")
        competitor_profiles = state.get("competitor_profiles")
        
        if not all([brand_profile, gap_analysis, metrics, competitor_profiles]):
            raise ValueError("Missing data for Growth Strategy.")
            
        print(f"[*] Generating Social Growth Strategy...")
        strategy = self.service.generate_growth_strategy(brand_profile, gap_analysis, metrics, competitor_profiles)
            
        return {"growth_strategy": strategy}
