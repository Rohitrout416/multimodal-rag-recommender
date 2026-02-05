from typing import List, Dict

class TrendService:
    def get_trends(self) -> List[Dict]:
        """
        Returns a list of trending fashion topics with metadata.
        """
        return [
            {
                "keyword": "Sustainable Denim",
                "score": 98,
                "change": "+12%",
                "image_url": "https://placehold.co/400x300/e0f2f1/00695c?text=Sustainable+Denim",
                "description": "Eco-friendly denim production is taking over the market."
            },
            {
                "keyword": "Oversized Blazers",
                "score": 85,
                "change": "+5%",
                "image_url": "https://placehold.co/400x300/f3e5f5/4a148c?text=Oversized+Blazers",
                "description": "The power suit is back, bigger and bolder than ever."
            },
            {
                "keyword": "Cyberpunk Aesthetics",
                "score": 92,
                "change": "+24%",
                "image_url": "https://placehold.co/400x300/212121/00e676?text=Cyberpunk",
                "description": "Neon accents and tech-wear materials are trending globally."
            },
            {
                "keyword": "Monochrome Beige",
                "score": 78,
                "change": "-2%",
                "image_url": "https://placehold.co/400x300/fff3e0/e65100?text=Beige+Tone",
                "description": "Minimalist earth tones remain a staple for the season."
            },
             {
                "keyword": "Y2K Revival",
                "score": 95,
                "change": "+18%",
                "image_url": "https://placehold.co/400x300/f8bbd0/880e4f?text=Y2K+Fashion",
                "description": "Low-rise jeans and butterfly clips are back in style."
            }
        ]

trend_service = TrendService()
