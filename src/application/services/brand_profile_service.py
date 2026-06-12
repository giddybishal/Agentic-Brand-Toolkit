from ...ports.llm_port import LLMPort
from ...domain.models.brand_profile import BrandProfile
from ...utils.prompts import BRAND_PROFILE_PROMPT

class BrandProfileService:
    def __init__(self, llm: LLMPort):
        self.llm = llm

    def generate_profile(self, content: str) -> BrandProfile:
        prompt = BRAND_PROFILE_PROMPT.format(content=content)
        return self.llm.generate_structured_data(prompt, BrandProfile)
