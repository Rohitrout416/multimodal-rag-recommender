from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = {}

class Product(BaseModel):
    id: int
    name: str
    description: str
    category: str
    price: float
    image_url: str

class ChatResponse(BaseModel):
    response: str
    products: List[Product] = []
