import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.adapters.gemini_adapter import GeminiAdapter
from src.application.services.strategy_service import StrategyService
from src.domain.models.brand_profile import BrandProfile
from src.domain.models.competitor import CompetitorProfile
from src.domain.models.analytics import EngagementMetrics, GapAnalysis

def main():
    print("Testing Growth Strategy...")
    llm = GeminiAdapter()
    service = StrategyService(llm)
    
    brand = BrandProfile(
        brand_name="EcoClean",
        industry="Eco-friendly Cleaning Products",
        mission="To save the earth one spray at a time.",
        description="We make non-toxic surface cleaners.",
        products=["All-purpose cleaner", "Glass cleaner"]
    )
    
    gap = GapAnalysis(
        content_gaps=["Lack of educational content compared to competitors"],
        positioning_gaps=["Seen as premium but failing to justify value"],
        branding_gaps=["Visuals are too sterile"],
        engagement_gaps=["Very low share rate"],
        opportunity_areas=["Leverage TikTok for quick cleaning hacks"]
    )
    
    print(f"Generating Growth Strategy for {brand.brand_name}...")
    strategy = service.generate_growth_strategy(brand, gap, [], [])
    
    print("\n--- Growth Strategy ---")
    print("Quick Wins:", strategy.quick_wins)
    print("Content Ideas:", strategy.content_ideas)
        
if __name__ == "__main__":
    main()
