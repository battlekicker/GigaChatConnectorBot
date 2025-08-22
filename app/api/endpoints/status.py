from fastapi import APIRouter
from app.models.schemas import StatusResponse
from app.services.context import context_service
from app.utils.logging import get_logger

router = APIRouter()
logger = get_logger("api.status")

@router.get("/status", response_model=StatusResponse)
async def get_status():
    logger.debug("Status endpoint accessed")

    status_data = {
        "status": "active",
        "service": "GigaChat API",
        "active_users": len(context_service.conversations)
    }

    logger.info(f"Status check: {status_data}")
    return status_data