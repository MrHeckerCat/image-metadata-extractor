# Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY image_metadata_extractor.py .

CMD [ "uvicorn", "image_metadata_extractor:app", "--host", "0.0.0.0", "--port", "8080" ]
