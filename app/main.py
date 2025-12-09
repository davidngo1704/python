from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

from app.routers import notification


app = FastAPI(title="Thành Đại")

Base.metadata.create_all(bind=engine)

app.include_router(notification.router, prefix="/notification", tags=["Notification"])
