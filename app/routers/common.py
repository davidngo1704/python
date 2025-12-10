from fastapi import APIRouter

from app.dainthuggingface.ultis import test

router = APIRouter()

@router.get("/")
def list_notification():
    return test()
