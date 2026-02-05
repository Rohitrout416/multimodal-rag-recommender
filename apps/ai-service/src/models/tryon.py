from pydantic import BaseModel
from typing import Optional

class TryOnRequest(BaseModel):
    user_image: str # Base64
    clothing_image: str # Base64

class TryOnResponse(BaseModel):
    result_image_url: str
