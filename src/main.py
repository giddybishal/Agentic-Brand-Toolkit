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

from src.application.tools import (
    CrawlTool,
    VisualIdentityTool,
    BrandProfileTool,
    CompetitorDiscoveryTool,
    CompetitorIntelligenceTool,
    SocialDatasetTool,
    EngagementAnalyticsTool,
    GapAnalysisTool,
    GrowthStrategyTool,
    CreatorGuidelinesTool,
    ToolkitBuilderTool,
    ResolveBrandIdentityTool,
    RequestHumanReviewTool
)
from src.application.agents.brand_intelligence_agent import BrandIntelligenceAgent
from langgraph.types import Command

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "what color palette does Drink Lucent use?"
    print(f"Starting Agentic Brand Toolkit Analysis for Query: '{query}'\n")

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

    # 3. Initialize Tools
    tools = [
        ResolveBrandIdentityTool(),
        CrawlTool(crawl_service),
        VisualIdentityTool(visual_service),
        BrandProfileTool(profile_service),
        CompetitorDiscoveryTool(competitor_service),
        CompetitorIntelligenceTool(competitor_service),
        SocialDatasetTool(social_service),
        EngagementAnalyticsTool(analytics_service),
        GapAnalysisTool(strategy_service),
        GrowthStrategyTool(strategy_service),
        CreatorGuidelinesTool(guidelines_service),
        ToolkitBuilderTool(toolkit_service),
        RequestHumanReviewTool()
    ]

    # 4. Build Agent
    agent = BrandIntelligenceAgent(tools)

    # 5. Run Graph
    output_dir = Path("data/current")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    comp_dir = output_dir / "competitors"
    social_dir = output_dir / "social_profiles"
    analytics_dir = output_dir / "analytics"
    
    initial_state = {"query": query}
    
    print("Executing workflow via ReAct Agent...")
    config = {"configurable": {"thread_id": "cli_run_1"}}
    state = agent.graph.invoke(initial_state, config)
    
    while True:
        snapshot = agent.graph.get_state(config)
        if not snapshot.next:
            break
            
        interrupts = snapshot.tasks[0].interrupts if snapshot.tasks else ()
        interrupt_value = interrupts[0].value if interrupts else "Graph paused. Please provide input to resume: "
        
        print("\n=== HUMAN-IN-THE-LOOP ===")
        user_input = input(f"{interrupt_value}\n> ")
        
        print("\nResuming graph execution...")
        state = agent.graph.invoke(Command(resume=user_input), config)
        
    final_state = state
    
    toolkit = final_state.get("toolkit")
    print("\nGeneration Complete!")
    
    # Save artifacts individually
    output_dir.mkdir(parents=True, exist_ok=True)
    
    toolkit = final_state.get("toolkit")
    if toolkit:
        with open(output_dir / "brand_toolkit.json", "w", encoding="utf-8") as f:
            f.write(toolkit.model_dump_json(indent=2))
            
    # Always save whatever partial artifacts exist in the final state
    competitor_profiles = final_state.get("competitor_profiles")
    if competitor_profiles:
        comp_dir.mkdir(parents=True, exist_ok=True)
        with open(comp_dir / "competitor_profiles.json", "w", encoding="utf-8") as f:
            # Handle both lists of pydantic models and raw dicts
            data = [c.model_dump() if hasattr(c, "model_dump") else c for c in competitor_profiles]
            f.write(json.dumps(data, indent=2))
            
    brand_social_profile = final_state.get("brand_social_profile")
    if brand_social_profile:
        social_dir.mkdir(parents=True, exist_ok=True)
        with open(social_dir / "brand_social_profile.json", "w", encoding="utf-8") as f:
            data = brand_social_profile.model_dump_json(indent=2) if hasattr(brand_social_profile, "model_dump_json") else json.dumps(brand_social_profile, indent=2)
            f.write(data)
            
    competitor_social_profiles = final_state.get("competitor_social_profiles")
    if competitor_social_profiles:
        social_dir.mkdir(parents=True, exist_ok=True)
        with open(social_dir / "competitor_social_profiles.json", "w", encoding="utf-8") as f:
            data = [s.model_dump() if hasattr(s, "model_dump") else s for s in competitor_social_profiles]
            f.write(json.dumps(data, indent=2))
            
    engagement_metrics = final_state.get("engagement_metrics")
    if engagement_metrics:
        analytics_dir.mkdir(parents=True, exist_ok=True)
        with open(analytics_dir / "engagement_metrics.json", "w", encoding="utf-8") as f:
            data = [m.model_dump() if hasattr(m, "model_dump") else m for m in engagement_metrics]
            f.write(json.dumps(data, indent=2))
            
    gap_analysis = final_state.get("gap_analysis")
    if gap_analysis:
        analytics_dir.mkdir(parents=True, exist_ok=True)
        with open(analytics_dir / "gap_analysis.json", "w", encoding="utf-8") as f:
            data = gap_analysis.model_dump_json(indent=2) if hasattr(gap_analysis, "model_dump_json") else json.dumps(gap_analysis, indent=2)
            f.write(data)
            
    growth_strategy = final_state.get("growth_strategy")
    if growth_strategy:
        analytics_dir.mkdir(parents=True, exist_ok=True)
        with open(analytics_dir / "growth_strategy.json", "w", encoding="utf-8") as f:
            data = growth_strategy.model_dump_json(indent=2) if hasattr(growth_strategy, "model_dump_json") else json.dumps(growth_strategy, indent=2)
            f.write(data)
            
    print(f"Artifacts saved to {output_dir}")

if __name__ == "__main__":
    main()
