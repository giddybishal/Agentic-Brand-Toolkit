from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.strategy_service import StrategyService

class GapAnalysisNode:
    def __init__(self, service: StrategyService):
        self.service = service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        brand_profile = state.get("brand_profile")
        metrics = state.get("engagement_metrics")
        competitor_profiles = state.get("competitor_profiles")
        
        if not all([brand_profile, metrics, competitor_profiles]):
            raise ValueError("Missing data for Gap Analysis.")
            
        print(f"[*] Performing Competitive Gap Analysis...")
        gap_analysis = self.service.analyze_gaps(brand_profile, metrics, competitor_profiles)
            
        return {"gap_analysis": gap_analysis}
