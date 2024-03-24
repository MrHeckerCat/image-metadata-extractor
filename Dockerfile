# Dockerfile
FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
    libimage-exiftool-perl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "image_metadata_extractor:app", "--host", "0.0.0.0", "--port", "8080" ]
