from fastapi import APIRouter, Depends
from typing import List

from app.schemas.notification_schema import NotificationCreate, NotificationUpdate, NotificationResponse
from app.services.notification_service import NotificationService, get_notification_service

router = APIRouter()

@router.post("/", response_model=NotificationResponse)
def create_notification(data: NotificationCreate, service: NotificationService = Depends(get_notification_service)):
    return service.create(data)

@router.get("/", response_model=List[NotificationResponse])
def list_notification(service: NotificationService = Depends(get_notification_service)):
    return service.get_all()

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(notification_id: int, service: NotificationService = Depends(get_notification_service)):
    return service.get_by_id(notification_id)

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    data: NotificationUpdate,
    service: NotificationService = Depends(get_notification_service)
):
    return service.update(notification_id, data)

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, service: NotificationUpdate = Depends(get_notification_service)):
    return service.delete(notification_id)