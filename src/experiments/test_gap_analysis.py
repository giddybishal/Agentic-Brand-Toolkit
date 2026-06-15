import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.adapters.gemini_adapter import GeminiAdapter
from src.application.services.strategy_service import StrategyService
from src.domain.models.brand_profile import BrandProfile
from src.domain.models.competitor import CompetitorProfile
from src.domain.models.analytics import EngagementMetrics

def main():
    print("Testing Gap Analysis...")
    llm = GeminiAdapter()
    service = StrategyService(llm)
    
    brand = BrandProfile(
        brand_name="EcoClean",
        industry="Eco-friendly Cleaning Products",
        mission="To save the earth one spray at a time.",
        description="We make non-toxic surface cleaners.",
        products=["All-purpose cleaner", "Glass cleaner"]
    )
    
    comp = CompetitorProfile(
        company_name="GreenWorks",
        positioning_summary="Established natural cleaner brand with wide retail distribution.",
        strengths=["Brand recognition", "Lower price point"],
        target_audience="Suburban families",
        content_strategy_summary="Focuses on family-oriented educational content and DIY cleaning tips."
    )
    
    brand_metrics = EngagementMetrics(
        brand_name="EcoClean",
        average_likes=120.5,
        average_comments=15.2,
        average_shares=5.0,
        posting_frequency="3 times a week",
        content_type_distribution={"Promotional": 0.8, "Educational": 0.2}
    )
    
    comp_metrics = EngagementMetrics(
        brand_name="GreenWorks",
        average_likes=850.0,
        average_comments=120.0,
        average_shares=45.0,
        posting_frequency="Daily",
        content_type_distribution={"Promotional": 0.3, "Educational": 0.5, "Customer Success": 0.2}
    )
    
    print(f"Generating Gap Analysis for {brand.brand_name} vs {comp.company_name}...")
    analysis = service.analyze_gaps(brand, [brand_metrics, comp_metrics], [comp])
    
    print("\n--- Gap Analysis ---")
    print("Content Gaps:", analysis.content_gaps)
    print("Opportunity Areas:", analysis.opportunity_areas)
        
if __name__ == "__main__":
    main()
