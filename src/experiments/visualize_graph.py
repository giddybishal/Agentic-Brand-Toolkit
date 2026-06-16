import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.application.agents.brand_intelligence_agent import BrandIntelligenceAgent
from src.application.tools import (
    CrawlTool, VisualIdentityTool, BrandProfileTool, CompetitorDiscoveryTool,
    CompetitorIntelligenceTool, SocialDatasetTool, EngagementAnalyticsTool,
    GapAnalysisTool, GrowthStrategyTool, CreatorGuidelinesTool, ToolkitBuilderTool,
    ResolveBrandIdentityTool, RequestHumanReviewTool
)

def main():
    tools = [
        ResolveBrandIdentityTool(),
        CrawlTool(None),
        VisualIdentityTool(None),
        BrandProfileTool(None),
        CompetitorDiscoveryTool(None),
        CompetitorIntelligenceTool(None),
        SocialDatasetTool(None),
        EngagementAnalyticsTool(None),
        GapAnalysisTool(None),
        GrowthStrategyTool(None),
        CreatorGuidelinesTool(None),
        ToolkitBuilderTool(None),
        RequestHumanReviewTool()
    ]

    agent = BrandIntelligenceAgent(tools)
    graph = agent.graph

    output_dir = Path("data/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        mermaid_png = graph.get_graph().draw_mermaid_png()
        with open(output_dir / "agent_graph.png", "wb") as f:
            f.write(mermaid_png)
        print(f"Successfully saved graph visualization to {output_dir / 'agent_graph.png'}")
    except Exception as e:
        print(f"Failed to generate PNG (requires Graphviz/Mermaid dependencies): {e}")

    try:
        mermaid_text = graph.get_graph().draw_mermaid()
        with open(output_dir / "agent_graph.md", "w") as f:
            f.write(f"```mermaid\n{mermaid_text}\n```")
        print(f"Successfully saved mermaid diagram to {output_dir / 'agent_graph.md'}")
    except Exception as e:
        print(f"Failed to generate Mermaid text: {e}")

if __name__ == "__main__":
    main()
