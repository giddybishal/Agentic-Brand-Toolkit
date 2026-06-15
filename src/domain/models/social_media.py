from pydantic import BaseModel
from typing import List

class SocialPost(BaseModel):
    caption: str
    image_description: str
    likes: int
    comments: int
    shares: int
    post_date: str
    content_type: str

class SocialMediaProfile(BaseModel):
    brand_name: str
    posts: List[SocialPost]
