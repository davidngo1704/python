from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

from app.routers import notification, common, chat


app = FastAPI(title="Thành Đại")

Base.metadata.create_all(bind=engine)

app.include_router(notification.router, prefix="/notification", tags=["notification"])
app.include_router(common.router, prefix="/common", tags=["common"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])