FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p /app/data

COPY . .

RUN chmod +x /app/entrypoint.sh

CMD ["./entrypoint.sh"]
