from ...ports.visual_extraction_port import ColorExtractorPort, LogoExtractorPort
from ...domain.models.visual_identity import VisualIdentity

class VisualIdentityService:
    def __init__(self, color_extractor: ColorExtractorPort, logo_extractor: LogoExtractorPort):
        self.color_extractor = color_extractor
        self.logo_extractor = logo_extractor

    def extract_visual_identity(self, url: str) -> VisualIdentity:
        colors, typography = self.color_extractor.extract_colors(url)
        logo_result = self.logo_extractor.extract_logos(url)
        logo_urls = [logo_result.get("logo_url")] if logo_result and logo_result.get("logo_url") else []
        return VisualIdentity(color_palette=colors, typography=typography, logo_urls=logo_urls)
