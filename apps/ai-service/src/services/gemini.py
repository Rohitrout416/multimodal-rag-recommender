import google.generativeai as genai
import os
import time
from typing import Optional, List, Dict, Any

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.model = None
        self.vision_model = None
        
        if not api_key:
            print("Warning: GOOGLE_API_KEY not set")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.vision_model = genai.GenerativeModel('gemini-2.5-flash')


    async def generate_text(self, prompt: str, max_retries: int = 2) -> str:
        """
        Generate text response from Gemini with retry on rate limit
        """
        if not self.model:
            return "Gemini model is not configured. Please check your API key."
        
        for attempt in range(max_retries + 1):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                error_str = str(e)
                # Retry on rate limit (429) errors
                if "429" in error_str and attempt < max_retries:
                    wait_time = (attempt + 1) * 5  # 5s, 10s
                    print(f"Rate limited, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue
                print(f"Error generating text: {e}")
                return "I apologize, but I am unable to process your request at the moment. Please try again in a few seconds."

    async def generate_with_images(self, prompt: str, images: List[Any]) -> str:
        """
        Generate response from Gemini with images
        """
        try:
            content = [prompt] + images
            response = self.vision_model.generate_content(content)
            return response.text
        except Exception as e:
            print(f"Error generating with images: {e}")
            return "I apologize, but I am unable to analyze the images at the moment."

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text using gemini-embedding-001
        """
        for attempt in range(3):
            try:
                result = genai.embed_content(
                    model="models/gemini-embedding-001",
                    content=text,
                    task_type="RETRIEVAL_QUERY"
                )
                return result['embedding']
            except Exception as e:
                error_str = str(e)
                if "429" in error_str and attempt < 2:
                    time.sleep((attempt + 1) * 3)
                    continue
                print(f"Error embedding text: {e}")
                return []

gemini_service = GeminiService()
