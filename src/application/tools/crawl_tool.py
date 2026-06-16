from typing import Dict, Any, Type
from pydantic import BaseModel, Field
from .base_tool import BrandTool
from ..services.crawl_service import CrawlService

class CrawlToolSchema(BaseModel):
    url: str = Field(description="The website URL to crawl")

class CrawlTool(BrandTool):
    name = "crawl_website"
    description = """
    Dependency:
    - Requires: website_url (Resolved brand URL)
    - Produces: website_content (raw website text)
    - Used by: extract_visual_identity, generate_brand_profile
    
    Rule: DO NOT use if website_content is already Present. Only use if explicit content crawling is required.
        """
    args_schema = CrawlToolSchema

    def __init__(self, crawl_service: CrawlService):
        self.crawl_service = crawl_service

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        url = args.get("url")
        if not url:
            url = state.get("website_url", "")
        
        print(f"[*] Tool executing: Crawling website: {url} ...")
        content = self.crawl_service.crawl_website(url)
        
        return {
            "website_content": content,
            "tool_message": f"Successfully crawled {url}. Website content has been extracted and saved to memory. You can now use this content for visual identity or brand profile generation."
        }
