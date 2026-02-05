from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.db.mongodb import db
from src.api import auth, chat, tryon, trends

app = FastAPI(
    title="FashNet Backend API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    db.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    db.disconnect()

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(tryon.router, prefix=f"{settings.API_V1_STR}/try-on", tags=["try-on"])
app.include_router(trends.router, prefix=f"{settings.API_V1_STR}/trends", tags=["trends"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FashNet Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

