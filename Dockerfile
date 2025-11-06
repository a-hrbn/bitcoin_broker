FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt update && apt install -y iputils-ping && rm -rf /var/lib/apt/lists/*

COPY app.py .

CMD ["python", "app.py"]