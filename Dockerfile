FROM python:3.9-slim

WORKDIR /app

RUN pip install --upgrade pip && \
        pip install --no-cache-dir PySide6==6.4.2 ultralytics==8.1.0 numpy==1.26.4

COPY . .

CMD ["python", "src/main.py"]