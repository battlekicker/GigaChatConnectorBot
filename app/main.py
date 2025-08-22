from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import chat, status
from app.utils.logging import setup_logging

setup_logging()

from app.utils.logging import get_logger
logger = get_logger("main")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status.router, prefix="/api/v1", tags=["status"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup completed")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown initiated")

@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"message": "GigaChat API Service is running"}