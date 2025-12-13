from fastapi import APIRouter

from app.dainthuggingface.chat_manager import ChatManager
from app.schemas.common_schema import SingleChatModel


router = APIRouter()

chat = ChatManager()

@router.post("/")
def list_notification(data: SingleChatModel):
    return chat.chat(data.message)