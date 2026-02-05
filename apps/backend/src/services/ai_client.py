import httpx
from src.core.config import settings

class AIClient:
    def __init__(self):
        self.base_url = settings.MODEL_SERVICE_URL

    async def generate_response(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={"prompt": prompt},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()["text"]
            except Exception as e:
                print(f"Error calling AI service: {e}")
                return "I'm having trouble connecting to my fashion brain right now. Please try again."

ai_client = AIClient()
