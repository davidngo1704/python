from pydantic import BaseModel


class ChatModel(BaseModel):
    systemPrompt: str
    message: str

class Config:
    from_attributes = True