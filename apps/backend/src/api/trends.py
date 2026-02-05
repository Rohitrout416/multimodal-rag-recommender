from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from src.services.ai_client import ai_client

router = APIRouter()

@router.get("/")
async def get_trends():
    """
    Get current fashion trends.
    """
    try:
        trends = await ai_client.get_trends()
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
