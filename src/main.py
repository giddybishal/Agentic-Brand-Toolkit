import sys
import json
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

from src.application.graph.nodes.crawl_node import CrawlNode
from src.application.graph.nodes.visual_identity_node import VisualIdentityNode
from src.application.graph.nodes.brand_profile_node import BrandProfileNode
from src.application.graph.nodes.creator_guidelines_node import CreatorGuidelinesNode
from src.application.graph.nodes.toolkit_builder_node import ToolkitBuilderNode
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

    # 3. Initialize Nodes
    crawl_node = CrawlNode(crawl_service)
    visual_node = VisualIdentityNode(visual_service)
    profile_node = BrandProfileNode(profile_service)
    guidelines_node = CreatorGuidelinesNode(guidelines_service)
    toolkit_node = ToolkitBuilderNode(toolkit_service)

    # 4. Build Graph
    builder = BrandToolkitGraphBuilder(
        crawl_node=crawl_node,
        visual_node=visual_node,
        profile_node=profile_node,
        guidelines_node=guidelines_node,
        toolkit_node=toolkit_node
    )
    graph = builder.build()

    # 5. Run Graph
    initial_state = {"website_url": url}
    
    print("Executing workflow...")
    final_state = graph.invoke(initial_state)
    
    toolkit = final_state.get("toolkit")
    if not toolkit:
        print("Failed to generate toolkit.")
        return

    print("\n--- Brand Profile ---")
    if toolkit.brand_profile:
        print(toolkit.brand_profile.model_dump_json(indent=2))
        
    print("\n--- Visual Identity ---")
    if toolkit.visual_identity:
        print(toolkit.visual_identity.model_dump_json(indent=2))
        
    print("\n--- Creator Guidelines ---")
    if toolkit.creator_guidelines:
        print(toolkit.creator_guidelines.model_dump_json(indent=2))

    print("\nGeneration Complete!")
    
    # Save output
    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "brand_toolkit.json"
    
    with open(output_path, "w") as f:
        f.write(toolkit.model_dump_json(indent=2))
        
    print(f"Toolkit saved to {output_path}")

if __name__ == "__main__":
    main()
