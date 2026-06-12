from typing import Dict, Any
from ....domain.models.graph_state import BrandState
from ...services.crawl_service import CrawlService

class CrawlNode:
    def __init__(self, crawl_service: CrawlService):
        self.crawl_service = crawl_service

    def __call__(self, state: BrandState) -> Dict[str, Any]:
        url = state.get("website_url", "")
        print(f"[*] Crawling website: {url} ...")
        content = self.crawl_service.crawl_website(url)
        return {"website_content": content}
