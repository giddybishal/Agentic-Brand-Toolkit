from abc import ABC, abstractmethod

class CrawlerPort(ABC):
    @abstractmethod
    def crawl(self, url: str) -> str:
        pass
