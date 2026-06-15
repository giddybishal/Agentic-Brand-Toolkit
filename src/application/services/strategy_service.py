import json
from typing import List, Dict, Any
from ...domain.models.analytics import GapAnalysis, GrowthStrategy, EngagementMetrics
from ...domain.models.brand_profile import BrandProfile
from ...domain.models.competitor import CompetitorProfile
from ...ports.llm_port import LLMPort
from ...utils.prompts import GAP_ANALYSIS_PROMPT, GROWTH_STRATEGY_PROMPT

class StrategyService:
    def __init__(self, llm: LLMPort):
        self.llm = llm

    def analyze_gaps(self, brand_profile: BrandProfile, metrics: List[EngagementMetrics], competitor_profiles: List[CompetitorProfile]) -> GapAnalysis:
        metrics_dump = [m.model_dump() for m in metrics]
        comp_dump = [c.model_dump() for c in competitor_profiles]
        
        prompt = GAP_ANALYSIS_PROMPT.format(
            brand_profile=brand_profile.model_dump_json(indent=2),
            metrics=json.dumps(metrics_dump, indent=2),
            competitor_profiles=json.dumps(comp_dump, indent=2)
        )
        return self.llm.generate_structured_data(prompt, GapAnalysis)

    def generate_growth_strategy(self, brand_profile: BrandProfile, gap_analysis: GapAnalysis, metrics: List[EngagementMetrics], competitor_profiles: List[CompetitorProfile]) -> GrowthStrategy:
        context_data = {
            "brand_profile": brand_profile.model_dump(),
            "gap_analysis": gap_analysis.model_dump(),
            "engagement_metrics": [m.model_dump() for m in metrics],
            "competitors": [c.model_dump() for c in competitor_profiles]
        }
        
        prompt = GROWTH_STRATEGY_PROMPT.format(
            context_data=json.dumps(context_data, indent=2)
        )
        return self.llm.generate_structured_data(prompt, GrowthStrategy)
