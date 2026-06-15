from typing import List
from ...domain.models.competitor import Competitor, CompetitorList, CompetitorProfile
from ...domain.models.brand_profile import BrandProfile
from ...ports.llm_port import LLMPort
from ...utils.prompts import COMPETITOR_DISCOVERY_PROMPT, COMPETITOR_INTELLIGENCE_PROMPT

class CompetitorDiscoveryService:
    def __init__(self, llm: LLMPort):
        self.llm = llm

    def discover_competitors(self, brand_profile: BrandProfile) -> List[Competitor]:
        prompt = COMPETITOR_DISCOVERY_PROMPT.format(
            brand_profile=brand_profile.model_dump_json(indent=2)
        )
        result = self.llm.generate_structured_data(prompt, CompetitorList)
        return result.competitors

    def generate_competitor_profile(self, competitor: Competitor) -> CompetitorProfile:
        prompt = COMPETITOR_INTELLIGENCE_PROMPT.format(
            competitor_name=competitor.name,
            competitor_context=f"Industry: {competitor.industry}. Reasoning: {competitor.reasoning}"
        )
        return self.llm.generate_structured_data(prompt, CompetitorProfile)
