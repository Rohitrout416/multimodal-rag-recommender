from pydantic import BaseModel

class TryOnRequest(BaseModel):
    user_image: str  # Base64 string
    clothing_image: str # Base64 string

class TryOnResponse(BaseModel):
    result_image_url: str
