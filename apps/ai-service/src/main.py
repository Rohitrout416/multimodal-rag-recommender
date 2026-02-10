from fastapi import FastAPI, HTTPException
from src.services.gemini import gemini_service
from src.services.qdrant import vector_service
from src.models.generate import GenerateRequest, GenerateResponse, RagChatRequest, RagChatResponse, Product
import json

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    vector_service.ensure_collection()
    yield

app = FastAPI(title="FashNet AI Service", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to FashNet AI Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/generate", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest):
    try:
        text = await gemini_service.generate_text(request.prompt)
        return GenerateResponse(text=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag-chat", response_model=RagChatResponse)
async def chat_with_rag(request: RagChatRequest):
    try:
        # 1. Embed query (using Gemini embedding-001)
        query_embedding = await gemini_service.embed_text(request.query)
        
        if not query_embedding:
            # Fallback to pure generation if embedding fails
            text = await gemini_service.generate_text(request.query)
            return RagChatResponse(response=text, products=[])

        # 2. Search Qdrant
        search_results = vector_service.search(query_embedding, limit=3)
        
        # 3. Construct Context
        products_context = ""
        products_list = []
        for item in search_results:
            products_context += f"- {item['name']} (${item['price']}): {item['description']}\n"
            products_list.append(Product(
                id=item.get('id', 0), # Fallback ID
                name=item['name'],
                description=item['description'],
                category=item['category'],
                price=item['price'],
                image_url=item['image_url']
            ))
        
        # 4. Generate Answer
        prompt = f"""
        User Query: "{request.query}"
        
        Available Products from our Catalog:
        {products_context}
        
        Role: You are an expert fashion stylist.
        Task: Answer the user's query. If the available products are relevant, recommend them enthusiastically. 
        If no products are relevant, give general fashion advice but mention we don't have specific stock right now.
        Do not invent products not listed above.
        """
        
        response_text = await gemini_service.generate_text(prompt)
        
        return RagChatResponse(response=response_text, products=products_list)
        
    except Exception as e:
        print(f"RAG Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Milestone 4 Endpoints ---

from src.services.tryon import tryon_service
from src.models.tryon import TryOnRequest, TryOnResponse
from src.services.trends import trend_service

@app.post("/try-on", response_model=TryOnResponse)
async def try_on(request: TryOnRequest):
    try:
        result_url = await tryon_service.generate_tryon(request.user_image, request.clothing_image)
        return TryOnResponse(result_image_url=result_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trends")
async def get_trends():
    try:
        return trend_service.get_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

