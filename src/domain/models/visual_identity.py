from typing import List, Optional
from pydantic import BaseModel

class ColorPalette(BaseModel):
    primary: List[str] = []
    secondary: List[str] = []

class Typography(BaseModel):
    heading_font: Optional[str] = None
    body_font: Optional[str] = None

class VisualIdentity(BaseModel):
    logo_urls: List[str] = []
    color_palette: ColorPalette = ColorPalette()
    typography: Typography = Typography()
