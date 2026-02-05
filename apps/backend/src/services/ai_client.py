import httpx
from src.core.config import settings

class AIClient:
    def __init__(self):
        self.base_url = settings.MODEL_SERVICE_URL

    async def try_on(self, user_image: str, clothing_image: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/try-on",
                    json={"user_image": user_image, "clothing_image": clothing_image},
                    timeout=60.0 # Longer timeout for image processing
                )
                response.raise_for_status()
                return response.json()["result_image_url"]
            except Exception as e:
                print(f"Error calling AI service (Try-On): {e}")
                raise e

    async def get_trends(self) -> list:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/trends",
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error calling AI service (Trends): {e}")
                return []

ai_client = AIClient()
