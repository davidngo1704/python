from fastapi import APIRouter

from app.dainthuggingface.ultis import chat

router = APIRouter()

@router.get("/")
def list_notification(system: str, user: str):
    return chat(system, user)
