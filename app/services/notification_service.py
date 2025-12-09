from app.services.base_service import BaseService
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db

from app.models.notification_model import Notification

class NotificationService(BaseService):
    model = Notification

def get_notification_service(db: Session = Depends(get_db)):
    return NotificationService(db)
