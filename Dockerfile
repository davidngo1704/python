FROM python:3.12-slim

# Giữ root (mặc định)
USER root

# Tối ưu cache: nhóm các lệnh apt vào 1 layer để tránh invalidation
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        cmake \
        git \
        pkg-config \
        libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- PHẦN QUAN TRỌNG: tối ưu cache pip ---
# Chỉ copy requirements.txt trước
COPY requirements.txt .

# Cài pip nâng cấp (ít thay đổi, cache tốt)
RUN pip install --upgrade pip setuptools wheel

# Set biến môi trường build llama-cpp-python
ENV CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS"
ENV FORCE_CMAKE=1

# Cài dependencies -> bước này được cache *miễn là không đổi requirements.txt*
RUN pip install --no-cache-dir -r requirements.txt

# Bây giờ mới copy toàn bộ code (để thay đổi code không phá cache pip)
COPY . .

RUN mkdir -p /app/data
RUN chmod +x /app/entrypoint.sh

CMD ["./entrypoint.sh"]
