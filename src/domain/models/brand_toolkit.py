from pydantic import BaseModel
from typing import Optional
from .visual_identity import VisualIdentity
from .brand_profile import BrandProfile
from .creator_guidelines import CreatorGuidelines

class BrandToolkit(BaseModel):
    website_url: str
    brand_profile: Optional[BrandProfile] = None
    visual_identity: Optional[VisualIdentity] = None
    creator_guidelines: Optional[CreatorGuidelines] = None
