FROM python:3.12-slim

# Install system-level dependencies required for building llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    cmake \
    git \
    pkg-config \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Enable BLAS acceleration for llama-cpp-python
ENV CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS"
ENV FORCE_CMAKE=1

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/data

COPY . .

RUN chmod +x /app/entrypoint.sh

CMD ["./entrypoint.sh"]
