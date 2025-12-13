from fastapi import APIRouter

from app.dainthuggingface.memory import MemoryStore


router = APIRouter()

memory = MemoryStore()

@router.get("/")
def get_notification():
    return memory.get_all_messages()