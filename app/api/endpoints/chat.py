from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import asyncio
import json
from app.models.schemas import ChatRequest, ChatResponse
from app.services.context import context_service
from app.services.gigachat_service import gigachat_service
from app.utils.logging import get_logger

router = APIRouter()
logger = get_logger("api.chat")


async def generate_streaming_response(messages: list, user_id: str):
    try:
        logger.info(f"Generating stream for user {user_id}")

        response_text = gigachat_service.get_response(messages)
        logger.info(f"Generated response length: {len(response_text)}")

        words = response_text.split()

        for i, word in enumerate(words):
            # Отправляем каждое слово с пробелом
            chunk = word + (" " if i < len(words) - 1 else "")
            yield f"data: {json.dumps({'chunk': chunk, 'complete': False})}\n\n"
            await asyncio.sleep(0.1)  # Задержка для эффекта печати

        yield f"data: {json.dumps({'complete': True})}\n\n"

        context_service.add_message(user_id, "assistant", response_text)
        logger.info(f"Stream completed for user {user_id}")

    except Exception as e:
        error_msg = f"Error in streaming: {str(e)}"
        logger.error(error_msg)
        yield f"data: {json.dumps({'error': error_msg, 'complete': True})}\n\n"


@router.post("/chat", response_model=ChatResponse)
async def chat_with_gigachat(request: ChatRequest):
    try:
        logger.info(f"Chat request from user {request.user_id}")

        context_service.add_message(request.user_id, "user", request.message)

        messages = context_service.get_context(request.user_id)

        return StreamingResponse(
            generate_streaming_response(messages, request.user_id),
            media_type="text/event-stream"
        )

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))