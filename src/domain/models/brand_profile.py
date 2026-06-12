from pydantic import BaseModel
from typing import List

class BrandProfile(BaseModel):
    brand_name: str = ""
    industry: str = ""
    mission: str = ""
    description: str = ""
    products: List[str] = []
