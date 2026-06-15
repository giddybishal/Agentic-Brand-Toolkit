import sys
import json
import shutil
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.adapters.crawler_adapter import CrawlerAdapter
from src.adapters.color_extractor_adapter import ColorExtractorAdapter
from src.adapters.logo_extractor_adapter import LogoExtractorAdapter
from src.adapters.gemini_adapter import GeminiAdapter

from src.application.services.crawl_service import CrawlService
from src.application.services.visual_identity_service import VisualIdentityService
from src.application.services.brand_profile_service import BrandProfileService
from src.application.services.creator_guidelines_service import CreatorGuidelinesService
from src.application.services.toolkit_service import ToolkitService
from src.application.services.competitor_service import CompetitorDiscoveryService
from src.application.services.social_simulation_service import SocialSimulationService
from src.application.services.analytics_service import EngagementAnalyticsService
from src.application.services.strategy_service import StrategyService

from src.application.graph.nodes.crawl_node import CrawlNode
from src.application.graph.nodes.visual_identity_node import VisualIdentityNode
from src.application.graph.nodes.brand_profile_node import BrandProfileNode
from src.application.graph.nodes.creator_guidelines_node import CreatorGuidelinesNode
from src.application.graph.nodes.toolkit_builder_node import ToolkitBuilderNode
from src.application.graph.nodes.competitor_discovery_node import CompetitorDiscoveryNode
from src.application.graph.nodes.competitor_intelligence_node import CompetitorIntelligenceNode
from src.application.graph.nodes.social_dataset_node import SocialDatasetNode
from src.application.graph.nodes.engagement_analytics_node import EngagementAnalyticsNode
from src.application.graph.nodes.gap_analysis_node import GapAnalysisNode
from src.application.graph.nodes.growth_strategy_node import GrowthStrategyNode

from src.application.graph.graph_builder import BrandToolkitGraphBuilder

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.drinklucent.com/"
    print(f"Starting Agentic Brand Toolkit Generation for URL: {url}\n")

    # 1. Initialize Adapters
    crawler = CrawlerAdapter()
    color_extractor = ColorExtractorAdapter()
    logo_extractor = LogoExtractorAdapter()
    llm = GeminiAdapter()

    # 2. Initialize Services
    crawl_service = CrawlService(crawler)
    visual_service = VisualIdentityService(color_extractor, logo_extractor)
    profile_service = BrandProfileService(llm)
    guidelines_service = CreatorGuidelinesService(llm)
    toolkit_service = ToolkitService()
    
    competitor_service = CompetitorDiscoveryService(llm)
    social_service = SocialSimulationService(llm)
    analytics_service = EngagementAnalyticsService()
    strategy_service = StrategyService(llm)

    # 3. Initialize Nodes
    crawl_node = CrawlNode(crawl_service)
    visual_node = VisualIdentityNode(visual_service)
    profile_node = BrandProfileNode(profile_service)
    guidelines_node = CreatorGuidelinesNode(guidelines_service)
    toolkit_node = ToolkitBuilderNode(toolkit_service)
    
    comp_discovery_node = CompetitorDiscoveryNode(competitor_service)
    comp_intel_node = CompetitorIntelligenceNode(competitor_service)
    social_node = SocialDatasetNode(social_service)
    analytics_node = EngagementAnalyticsNode(analytics_service)
    gap_node = GapAnalysisNode(strategy_service)
    growth_node = GrowthStrategyNode(strategy_service)

    # 4. Build Graph
    builder = BrandToolkitGraphBuilder(
        crawl_node=crawl_node,
        visual_node=visual_node,
        profile_node=profile_node,
        competitor_discovery_node=comp_discovery_node,
        competitor_intelligence_node=comp_intel_node,
        social_dataset_node=social_node,
        engagement_analytics_node=analytics_node,
        gap_analysis_node=gap_node,
        growth_strategy_node=growth_node,
        guidelines_node=guidelines_node,
        toolkit_node=toolkit_node
    )
    graph = builder.build()

    # 5. Run Graph
    # Clear previous artifacts
    output_dir = Path("data/current")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    comp_dir = output_dir / "competitors"
    social_dir = output_dir / "social_profiles"
    analytics_dir = output_dir / "analytics"
    
    comp_dir.mkdir(exist_ok=True)
    social_dir.mkdir(exist_ok=True)
    analytics_dir.mkdir(exist_ok=True)
    
    initial_state = {"website_url": url}
    
    print("Executing workflow...")
    final_state = graph.invoke(initial_state)
    
    toolkit = final_state.get("toolkit")
    if not toolkit:
        print("Failed to generate toolkit.")
        return

    print("\nGeneration Complete!")
    
    # Save artifacts individually
    with open(output_dir / "brand_toolkit.json", "w", encoding="utf-8") as f:
        f.write(toolkit.model_dump_json(indent=2))
        
    if toolkit.competitor_profiles:
        with open(comp_dir / "competitor_profiles.json", "w", encoding="utf-8") as f:
            f.write(json.dumps([c.model_dump() for c in toolkit.competitor_profiles], indent=2))
            
    if toolkit.brand_social_profile:
        with open(social_dir / "brand_social_profile.json", "w", encoding="utf-8") as f:
            f.write(toolkit.brand_social_profile.model_dump_json(indent=2))
            
    if toolkit.competitor_social_profiles:
        with open(social_dir / "competitor_social_profiles.json", "w", encoding="utf-8") as f:
            f.write(json.dumps([s.model_dump() for s in toolkit.competitor_social_profiles], indent=2))
            
    if toolkit.engagement_metrics:
        with open(analytics_dir / "engagement_metrics.json", "w", encoding="utf-8") as f:
            f.write(json.dumps([m.model_dump() for m in toolkit.engagement_metrics], indent=2))
            
    if toolkit.gap_analysis:
        with open(analytics_dir / "gap_analysis.json", "w", encoding="utf-8") as f:
            f.write(toolkit.gap_analysis.model_dump_json(indent=2))
            
    if toolkit.growth_strategy:
        with open(analytics_dir / "growth_strategy.json", "w", encoding="utf-8") as f:
            f.write(toolkit.growth_strategy.model_dump_json(indent=2))
            
    print(f"Toolkit and artifacts saved to {output_dir}")

if __name__ == "__main__":
    main()
