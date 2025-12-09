from pydantic import BaseModel

class NotificationCreate(BaseModel):
    code: str
    name: str
    type: str
    description: str

class NotificationUpdate(BaseModel):
    code: str | None
    name: str | None
    type: str | None
    description: str | None


class NotificationResponse(BaseModel):
    id: int
    code: str
    name: str
    type: str
    description: str

class Config:
    from_attributes = True