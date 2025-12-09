from fastapi import HTTPException
from sqlalchemy.orm import Session

class BaseService:
    model = None  # Model SQLAlchemy, service con phải gán

    def __init__(self, db: Session):
        self.db = db

    # Lấy toàn bộ
    def get_all(self):
        return self.db.query(self.model).all()

    # Lấy theo ID
    def get_by_id(self, obj_id: int):
        obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return obj

    # Tạo mới
    def create(self, data):
        obj = self.model(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    # Cập nhật
    def update(self, obj_id: int, data):
        obj = self.get_by_id(obj_id)
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    # Xóa
    def delete(self, obj_id: int):
        obj = self.get_by_id(obj_id)
        self.db.delete(obj)
        self.db.commit()
        return {"message": f"{self.model.__name__} deleted"}
