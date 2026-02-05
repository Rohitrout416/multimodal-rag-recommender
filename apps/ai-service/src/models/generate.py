from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class GenerateRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = None

class GenerateResponse(BaseModel):
    text: str

class RagChatRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

class Product(BaseModel):
    id: int
    name: str
    description: str
    category: str
    price: float
    image_url: str

class RagChatResponse(BaseModel):
    response: str
    products: List[Product]
