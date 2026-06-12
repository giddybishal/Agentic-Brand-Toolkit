import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.adapters.gemini_adapter import GeminiAdapter
from src.application.services.brand_profile_service import BrandProfileService

def test_brand_profile():
    llm = GeminiAdapter()
    service = BrandProfileService(llm)

    dummy_content = """
    Welcome to VeelApp. We are a next-generation social commerce platform designed specifically for Gen Z.
    Our mission is to empower creators to monetize their authentic content effortlessly. 
    We offer seamless in-app shopping, video-first product discovery, and instant payout for creators.
    """

    print("Generating Brand Profile...")
    profile = service.generate_profile(dummy_content)
    
    print("\n--- Brand Profile Output ---")
    print(profile.model_dump_json(indent=2))

if __name__ == "__main__":
    test_brand_profile()
