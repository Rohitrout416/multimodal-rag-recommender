import httpx
from src.core.config import settings

class AIClient:
    def __init__(self):
        self.base_url = settings.MODEL_SERVICE_URL

    async def chat_with_rag(self, query: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/rag-chat",
                    json={"query": query},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error calling AI service: {e}")
                return {
                    "response": "I'm having trouble connecting to my fashion brain right now. Please try again.",
                    "products": []
                }

ai_client = AIClient()
