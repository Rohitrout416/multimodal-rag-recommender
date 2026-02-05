from fastapi import APIRouter, Depends, HTTPException
from src.models.chat import ChatRequest, ChatResponse
from src.services.ai_client import ai_client
from src.api import deps
from src.models.user import UserResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: UserResponse = Depends(deps.get_current_user)
):
    """
    Chat with the AI Stylist.
    Auth required.
    """
    # Later: inject user preferences/wardrobe context into prompt
    prompt = f"User {current_user.username} says: {request.message}\n\nYou are a helpful AI Fashion Stylist. Respond to the user."
    
    response_text = await ai_client.generate_response(prompt)
    
    return ChatResponse(response=response_text)
