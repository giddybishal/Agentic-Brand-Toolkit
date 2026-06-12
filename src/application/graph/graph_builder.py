from langgraph.graph import StateGraph, END
from ...domain.models.graph_state import BrandState

class BrandToolkitGraphBuilder:
    def __init__(
        self,
        crawl_node,
        visual_node,
        profile_node,
        guidelines_node,
        toolkit_node
    ):
        self.crawl_node = crawl_node
        self.visual_node = visual_node
        self.profile_node = profile_node
        self.guidelines_node = guidelines_node
        self.toolkit_node = toolkit_node

    def build(self):
        workflow = StateGraph(BrandState)

        workflow.add_node("crawl", self.crawl_node)
        workflow.add_node("visual_identity", self.visual_node)
        workflow.add_node("brand_profile", self.profile_node)
        workflow.add_node("creator_guidelines", self.guidelines_node)
        workflow.add_node("toolkit_builder", self.toolkit_node)

        workflow.set_entry_point("crawl")

        workflow.add_edge("crawl", "visual_identity")
        workflow.add_edge("visual_identity", "brand_profile")
        workflow.add_edge("brand_profile", "creator_guidelines")
        workflow.add_edge("creator_guidelines", "toolkit_builder")
        workflow.add_edge("toolkit_builder", END)

        return workflow.compile()
