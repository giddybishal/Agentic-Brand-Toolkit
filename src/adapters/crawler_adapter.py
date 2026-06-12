from ..ports.crawler_port import CrawlerPort
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse

class CrawlerAdapter(CrawlerPort):
    def crawl(self, url: str) -> str:
        domain = urlparse(url).netloc or "unknown"
        outputs_dir = Path("data")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = outputs_dir / "screenshot.png"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            # Navigate and wait for network idle to ensure content is loaded
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception as e:
                print(f"Warning: Page load issue or timeout: {e}")
            
            page.screenshot(path=screenshot_path)
            html_content = page.content()
            browser.close()

        soup = BeautifulSoup(html_content, "html.parser")
        for script in soup(["script", "style", "noscript", "meta", "head", "title"]):
            script.extract()
        
        text = soup.get_text(separator=" ")
        # Clean up excessive whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return cleaned_text
