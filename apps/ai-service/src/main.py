from fastapi import FastAPI, HTTPException
from src.services.gemini import gemini_service
from src.models.generate import GenerateRequest, GenerateResponse

app = FastAPI(title="FashNet AI Service")

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

