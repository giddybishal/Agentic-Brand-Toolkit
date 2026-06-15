import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.adapters.gemini_adapter import GeminiAdapter
from src.application.services.competitor_service import CompetitorDiscoveryService
from src.domain.models.brand_profile import BrandProfile

def main():
    print("Testing Competitor Discovery Service...")
    llm = GeminiAdapter()
    service = CompetitorDiscoveryService(llm)
    
    dummy_profile = BrandProfile(
        brand_name="TechFlow",
        industry="B2B SaaS Project Management",
        mission="To streamline workflows for remote engineering teams.",
        description="TechFlow is a project management tool tailored for developers.",
        products=["Kanban boards", "Git integration", "Time tracking"]
    )
    
    print(f"Discovering competitors for: {dummy_profile.brand_name}...")
    competitors = service.discover_competitors(dummy_profile)
    for c in competitors:
        print(f"\n- {c.name} ({c.relevance_score}/100)")
        print(f"  Industry: {c.industry}")
        print(f"  Reasoning: {c.reasoning}")
        
if __name__ == "__main__":
    main()
