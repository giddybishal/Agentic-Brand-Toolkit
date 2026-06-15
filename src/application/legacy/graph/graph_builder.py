from langgraph.graph import StateGraph, END
from ...domain.models.graph_state import BrandState

class BrandToolkitGraphBuilder:
    def __init__(
        self,
        crawl_node,
        visual_node,
        profile_node,
        competitor_discovery_node,
        competitor_intelligence_node,
        social_dataset_node,
        engagement_analytics_node,
        gap_analysis_node,
        growth_strategy_node,
        guidelines_node,
        toolkit_node
    ):
        self.crawl_node = crawl_node
        self.visual_node = visual_node
        self.profile_node = profile_node
        self.competitor_discovery_node = competitor_discovery_node
        self.competitor_intelligence_node = competitor_intelligence_node
        self.social_dataset_node = social_dataset_node
        self.engagement_analytics_node = engagement_analytics_node
        self.gap_analysis_node = gap_analysis_node
        self.growth_strategy_node = growth_strategy_node
        self.guidelines_node = guidelines_node
        self.toolkit_node = toolkit_node

    def build(self):
        workflow = StateGraph(BrandState)

        workflow.add_node("crawl", self.crawl_node)
        workflow.add_node("visual_identity", self.visual_node)
        workflow.add_node("brand_profile", self.profile_node)
        workflow.add_node("competitor_discovery", self.competitor_discovery_node)
        workflow.add_node("competitor_intelligence", self.competitor_intelligence_node)
        workflow.add_node("social_dataset", self.social_dataset_node)
        workflow.add_node("engagement_analytics", self.engagement_analytics_node)
        workflow.add_node("gap_analysis", self.gap_analysis_node)
        workflow.add_node("growth_strategy", self.growth_strategy_node)
        workflow.add_node("creator_guidelines", self.guidelines_node)
        workflow.add_node("toolkit_builder", self.toolkit_node)

        workflow.set_entry_point("crawl")

        workflow.add_edge("crawl", "visual_identity")
        workflow.add_edge("visual_identity", "brand_profile")
        workflow.add_edge("brand_profile", "competitor_discovery")
        workflow.add_edge("competitor_discovery", "competitor_intelligence")
        workflow.add_edge("competitor_intelligence", "social_dataset")
        workflow.add_edge("social_dataset", "engagement_analytics")
        workflow.add_edge("engagement_analytics", "gap_analysis")
        workflow.add_edge("gap_analysis", "growth_strategy")
        workflow.add_edge("growth_strategy", "creator_guidelines")
        workflow.add_edge("creator_guidelines", "toolkit_builder")
        workflow.add_edge("toolkit_builder", END)

        return workflow.compile()
