from ...ports.llm_port import LLMPort
from ...domain.models.creator_guidelines import CreatorGuidelines
from ...domain.models.brand_profile import BrandProfile
from ...utils.prompts import CREATOR_GUIDELINES_PROMPT

class CreatorGuidelinesService:
    def __init__(self, llm: LLMPort):
        self.llm = llm

    def generate_guidelines(self, brand_profile: BrandProfile) -> CreatorGuidelines:
        # Convert the Pydantic model to a JSON string for the prompt
        profile_json = brand_profile.model_dump_json(indent=2)
        prompt = CREATOR_GUIDELINES_PROMPT.format(brand_profile=profile_json)
        return self.llm.generate_structured_data(prompt, CreatorGuidelines)
