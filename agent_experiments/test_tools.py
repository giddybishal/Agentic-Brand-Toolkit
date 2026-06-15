import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.adapters.crawler_adapter import CrawlerAdapter
from src.application.services.crawl_service import CrawlService
from src.application.tools.crawl_tool import CrawlTool

def main():
    print("Testing CrawlTool directly...")
    
    crawler = CrawlerAdapter()
    crawl_service = CrawlService(crawler)
    
    crawl_tool = CrawlTool(crawl_service)
    
    # Simulate agent state
    state = {"website_url": "https://www.drinklucent.com/"}
    args = {"url": "https://www.drinklucent.com/"}
    
    print(f"Inputs: {args}")
    result = crawl_tool.execute(state, args)
    
    print("\nOutput State Updates:")
    print("tool_message:", result.get("tool_message"))
    content = result.get("website_content", "")
    print(f"website_content length: {len(content)} chars")
    
    if len(content) > 0:
        print("\nTest Passed: Tool successfully wrapped the service and updated the state dictionary.")
    else:
        print("\nTest Failed: No content extracted.")

if __name__ == "__main__":
    main()
