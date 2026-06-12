from ...ports.crawler_port import CrawlerPort

class CrawlService:
    def __init__(self, crawler: CrawlerPort):
        self.crawler = crawler

    def crawl_website(self, url: str) -> str:
        return self.crawler.crawl(url)
