git config --global credential.helper store

python -m venv venv

.\venv\Scripts\Activate.ps1 (linux: source venv/bin/activate)

.\venv\Scripts\Activate.ps1

uvicorn app.main:app --reload
-----------------------------------------
mkdir -p /root/python_daint/data

chmod 777 /root/python_daint/data

touch /root/python_daint/data/data.db

chmod 666 /root/python_daint/data/data.db

alembic init migrations
-----------------------------------------
Quy trình migration sau khi thay đổi model

1. Đảm bảo DB URL:
   - Biến môi trường: DATABASE_URL (nếu không có thì Alembic dùng sqlite:///./data.db).
2. Tạo migration mới sau khi đổi model:
   - alembic revision --autogenerate -m "mo ta thay doi"
3. Kiểm tra file migration vừa tạo trong thư mục migrations/versions/.
4. Áp dụng migration lên database:
   - alembic upgrade head

-----------------------------------------
Chạy migration tự động khi chạy trong Docker

1. Image Docker đã cài sẵn alembic qua requirements.txt.
2. Script entrypoint sẽ chạy:
   - alembic upgrade head
   - sau đó chạy uvicorn app.main:app --host 0.0.0.0 --port 8000
3. Khi build và run container, DB sẽ tự động được migrate lên phiên bản mới nhất.

-----------------------------------------
Các bước rút gọn khi đổi schema

1. Sửa model / schema trong thư mục app/models, app/schemas.
2. Chạy: alembic revision --autogenerate -m "mo ta thay doi"
3. Kiểm tra file migration trong migrations/versions/
4. Chạy: alembic upgrade head
5. Build lại Docker image và deploy (entrypoint sẽ tự chạy migration khi container start).