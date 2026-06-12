import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.adapters.crawler_adapter import CrawlerAdapter

def test_crawler():
    url = "https://veelapp.com/"
    print(f"Testing CrawlerAdapter with URL: {url}")
    
    adapter = CrawlerAdapter()
    result = adapter.crawl(url)
    
    print("\n--- Extracted Text Preview ---")
    print(result[:500] + ("...\n" if len(result) > 500 else "\n"))
    print("--- End of Text ---")
    
    print("\nCheck data/screenshots for the generated screenshot.")

if __name__ == "__main__":
    test_crawler()
