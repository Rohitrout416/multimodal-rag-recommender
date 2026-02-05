from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict] = {}
    # Image support later

class ChatResponse(BaseModel):
    response: str
    # Later: suggested_products: List[Product]
