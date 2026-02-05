import google.generativeai as genai
import os
from typing import Optional, List, Dict, Any

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: GOOGLE_API_KEY not set")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.vision_model = genai.GenerativeModel('gemini-pro-vision')

    async def generate_text(self, prompt: str) -> str:
        """
        Generate text response from Gemini Pro
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return "I apologize, but I am unable to process your request at the moment."

    async def generate_with_images(self, prompt: str, images: List[Any]) -> str:
        """
        Generate response from Gemini Pro Vision with images
        """
        try:
            # images should be PIL Image objects or similar supported formats
            content = [prompt] + images
            response = self.vision_model.generate_content(content)
            return response.text
        except Exception as e:
            print(f"Error generating with images: {e}")
            return "I apologize, but I am unable to analyze the images at the moment."

gemini_service = GeminiService()
