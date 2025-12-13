from fastapi import APIRouter

from app.dainthuggingface.ultis import chat
from app.schemas.common_schema import ChatModel


router = APIRouter()

@router.post("/")
def list_notification(data: ChatModel):
    return chat(data.systemPrompt, data.message)

