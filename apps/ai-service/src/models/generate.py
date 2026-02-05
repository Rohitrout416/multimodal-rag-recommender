from pydantic import BaseModel
from typing import Optional, List

class GenerateRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = None
    # We will add image support later in RAG/Multimodal milestone

class GenerateResponse(BaseModel):
    text: str
