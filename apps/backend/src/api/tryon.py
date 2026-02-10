from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from src.models.tryon import TryOnResponse, TryOnRequest
from src.services.ai_client import ai_client
import base64

router = APIRouter()

@router.post("", response_model=TryOnResponse)
async def try_on(
    user_image: str = Form(...),
    clothing_image: str = Form(...)
):
    """
    Virtual Try-On Endpoint. 
    Accepts Base64 strings for simplicity in this milestone, or could be multipart files converted to base64.
    """
    try:
        # If the frontend sends raw base64 strings
        result_url = await ai_client.try_on(user_image, clothing_image)
        return TryOnResponse(result_image_url=result_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
