from ..ports.crawler_port import CrawlerPort
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse

class CrawlerAdapter(CrawlerPort):
    def _clean_text(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")
        for script in soup(["script", "style", "noscript", "meta", "head", "title"]):
            script.extract()
        
        text = soup.get_text(separator=" ")
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)

    def crawl(self, url: str) -> str:
        domain = urlparse(url).netloc or "unknown"
        outputs_dir = Path("data/current")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = outputs_dir / "screenshot.png"
        
        positive_keywords = ['about', 'services', 'products', 'solutions', 'company', 'mission', 'contact', 'careers']
        negative_keywords = ['login', 'privacy', 'terms', 'cookie', 'signin', 'signup']

        all_text_chunks = []
        visited_urls = set()
        pages_to_visit = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Crawl homepage
            print(f"  -> Crawling homepage: {url}")
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception as e:
                print(f"  -> Warning: Homepage load issue or timeout: {e}")
            
            page.screenshot(path=screenshot_path)
            html_content = page.content()
            visited_urls.add(url)
            
            # Extract links
            soup = BeautifulSoup(html_content, "html.parser")
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href'].lower()
                # Normalize href
                full_link = href
                if href.startswith('/'):
                    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
                    full_link = base_url + href
                    
                if not full_link.startswith('http'):
                    continue
                    
                # Check keywords
                if any(kw in href for kw in positive_keywords) and not any(kw in href for kw in negative_keywords):
                    if full_link not in visited_urls and full_link not in pages_to_visit:
                        pages_to_visit.append(full_link)
            
            # Extract text from homepage
            all_text_chunks.append(f"--- HOMEPAGE ---\n{self._clean_text(html_content)}")
            
            # Crawl subpages
            pages_to_visit = pages_to_visit[:5]
            for sub_url in pages_to_visit:
                print(f"  -> Crawling subpage: {sub_url}")
                try:
                    page.goto(sub_url, wait_until="networkidle", timeout=15000)
                    sub_html = page.content()
                    all_text_chunks.append(f"--- SUBPAGE: {sub_url} ---\n{self._clean_text(sub_html)}")
                    visited_urls.add(sub_url)
                except Exception as e:
                    print(f"  -> Warning: Failed to crawl {sub_url}: {e}")
            
            browser.close()

        combined_text = "\n\n".join(all_text_chunks)
        return combined_text
