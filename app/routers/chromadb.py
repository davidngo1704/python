from fastapi import APIRouter

from app.dainthuggingface.memory import MemoryStore
from app.schemas.common_schema import SingleChatModel

router = APIRouter()

memory = MemoryStore()

@router.get("/")
def get_notification():
    return memory.get_all_messages()

@router.post("/")
def list_notification(data: SingleChatModel):
    return memory.query(data.message)