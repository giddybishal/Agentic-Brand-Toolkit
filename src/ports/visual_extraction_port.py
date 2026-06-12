from abc import ABC, abstractmethod
from typing import List, Tuple
from ..domain.models.visual_identity import ColorPalette, Typography

class ColorExtractorPort(ABC):
    @abstractmethod
    def extract_colors(self, url: str) -> Tuple[ColorPalette, Typography]:
        pass

class LogoExtractorPort(ABC):
    @abstractmethod
    def extract_logos(self, url: str) -> dict:
        pass
