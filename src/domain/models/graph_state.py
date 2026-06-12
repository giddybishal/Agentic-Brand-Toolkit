from typing import TypedDict, Optional, Any
from .visual_identity import VisualIdentity
from .brand_profile import BrandProfile
from .creator_guidelines import CreatorGuidelines
from .brand_toolkit import BrandToolkit

class BrandState(TypedDict, total=False):
    website_url: str
    website_content: Optional[str]
    visual_identity: Optional[VisualIdentity]
    brand_profile: Optional[BrandProfile]
    creator_guidelines: Optional[CreatorGuidelines]
    toolkit: Optional[BrandToolkit]
