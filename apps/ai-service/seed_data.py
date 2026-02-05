import asyncio
import os
from src.services.gemini import gemini_service
from src.services.qdrant import vector_service

# Mock Data
MOCK_PRODUCTS = [
    {
        "name": "Floral Summer Dress",
        "description": "A light and breezy floral dress perfect for summer outings. Features a V-neck and short sleeves.",
        "category": "Dress",
        "price": 49.99,
        "image_url": "https://placehold.co/400x600/png?text=Floral+Dress"
    },
    {
        "name": "Classic Denim Jacket",
        "description": "Timeless denim jacket with a vintage wash. Great for layering in transitional weather.",
        "category": "Outerwear",
        "price": 89.99,
        "image_url": "https://placehold.co/400x600/png?text=Denim+Jacket"
    },
    {
        "name": "Red Evening Gown",
        "description": "Elegant red floor-length gown with a slit. Perfect for formal events and galas.",
        "category": "Dress",
        "price": 199.99,
        "image_url": "https://placehold.co/400x600/png?text=Red+Gown"
    },
    {
        "name": "White Sneakers",
        "description": "Clean and minimalist white sneakers. Comfortable for all-day wear.",
        "category": "Shoes",
        "price": 59.99,
        "image_url": "https://placehold.co/400x600/png?text=White+Sneakers"
    },
    {
        "name": "Leather Crossbody Bag",
        "description": "Genuine leather crossbody bag in black. Compact but spacious enough for essentials.",
        "category": "Accessories",
        "price": 129.50,
        "image_url": "https://placehold.co/400x600/png?text=Leather+Bag"
    }
]

async def seed():
    print("Starting data seeding...")
    
    # 1. Ensure Collection
    vector_service.ensure_collection()
    
    # 2. Generate Embeddings
    print("Generating embeddings...")
    embeddings = []
    for product in MOCK_PRODUCTS:
        # Create a rich text representation for embedding
        text_to_embed = f"{product['name']} {product['description']} Category: {product['category']}"
        embedding = await gemini_service.embed_text(text_to_embed)
        if embedding:
            embeddings.append(embedding)
        else:
            print(f"Failed to embed {product['name']}")
    
    # 3. Upsert to Qdrant
    if len(embeddings) == len(MOCK_PRODUCTS):
        print("Upserting to Qdrant...")
        vector_service.upsert_products(MOCK_PRODUCTS, embeddings)
        print("Seeding complete!")
    else:
        print("Mismatch in products and embeddings count. Aborting.")

if __name__ == "__main__":
    asyncio.run(seed())
