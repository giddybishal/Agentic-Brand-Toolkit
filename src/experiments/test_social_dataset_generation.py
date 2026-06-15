import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.adapters.gemini_adapter import GeminiAdapter
from src.application.services.social_simulation_service import SocialSimulationService
from src.domain.models.brand_profile import BrandProfile

def main():
    print("Testing Social Dataset Generation...")
    llm = GeminiAdapter()
    service = SocialSimulationService(llm)
    
    dummy_profile = BrandProfile(
        brand_name="TechFlow",
        industry="B2B SaaS Project Management",
        mission="To streamline workflows for remote engineering teams.",
        description="TechFlow is a project management tool tailored for developers.",
        products=["Kanban boards", "Git integration", "Time tracking"]
    )
    
    print(f"Simulating social profile for: {dummy_profile.brand_name}...")
    social_profile = service.simulate_social_profile(dummy_profile, dummy_profile.brand_name)
    
    print(f"\nGenerated {len(social_profile.posts)} posts.")
    for idx, post in enumerate(social_profile.posts[:3]):
        print(f"\nPost {idx+1} ({post.content_type}):")
        print(f"Date: {post.post_date}")
        print(f"Caption: {post.caption}")
        print(f"Image: {post.image_description}")
        print(f"Engagement: {post.likes} L | {post.comments} C | {post.shares} S")
        
if __name__ == "__main__":
    main()
