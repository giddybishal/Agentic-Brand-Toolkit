import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.adapters.gemini_adapter import GeminiAdapter
from src.application.services.creator_guidelines_service import CreatorGuidelinesService
from src.domain.models.brand_profile import BrandProfile

def test_creator_guidelines():
    llm = GeminiAdapter()
    service = CreatorGuidelinesService(llm)

    dummy_profile = BrandProfile(
        brand_name="VeelApp",
        industry="Social Commerce",
        mission="Empower creators to monetize their authentic content effortlessly.",
        description="A next-generation social commerce platform designed specifically for Gen Z, featuring seamless in-app shopping.",
        products=["In-app shopping", "Video-first product discovery", "Instant creator payouts"]
    )

    print("Generating Creator Guidelines...")
    guidelines = service.generate_guidelines(dummy_profile)
    
    print("\n--- Creator Guidelines Output ---")
    print(guidelines.model_dump_json(indent=2))

if __name__ == "__main__":
    test_creator_guidelines()
