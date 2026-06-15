from typing import List, Union
from ...domain.models.social_media import SocialMediaProfile, SocialPost
from ...domain.models.brand_profile import BrandProfile
from ...domain.models.competitor import CompetitorProfile
from ...ports.llm_port import LLMPort
from ...utils.prompts import SOCIAL_SIMULATION_PROMPT
from pydantic import BaseModel

class SocialPostList(BaseModel):
    posts: List[SocialPost]

class SocialSimulationService:
    def __init__(self, llm: LLMPort):
        self.llm = llm

    def simulate_social_profile(self, profile: Union[BrandProfile, CompetitorProfile], brand_name: str) -> SocialMediaProfile:
        prompt = SOCIAL_SIMULATION_PROMPT.format(
            profile_data=profile.model_dump_json(indent=2)
        )
        result = self.llm.generate_structured_data(prompt, SocialPostList)
        return SocialMediaProfile(
            brand_name=brand_name,
            posts=result.posts
        )
