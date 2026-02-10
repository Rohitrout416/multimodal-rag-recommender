from fastapi import APIRouter, Depends, HTTPException
from src.models.chat import ChatRequest, ChatResponse
from src.services.ai_client import ai_client
from src.api import deps
from src.models.user import UserResponse

router = APIRouter()

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: UserResponse = Depends(deps.get_current_user)
):
    """
    Chat with the AI Stylist (RAG Enabled).
    Auth required.
    """
    # Call the RAG pipeline
    result = await ai_client.chat_with_rag(request.message)
    
    return ChatResponse(
        response=result["response"],
        products=result.get("products", [])
    )
