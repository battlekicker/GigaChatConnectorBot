from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    user_id: str

class StatusResponse(BaseModel):
    status: str
    service: str
    active_users: int

class ChatResponse(BaseModel):
    response: str
    user_id: str
    message_count: int
    context_size: str

class ErrorResponse(BaseModel):
    error: str
    details: str = None