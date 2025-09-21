# backend/Dockerfile.alpine
FROM python:3.10-alpine

WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache \
    libglib \
    libsm \
    libxext \
    libxrender \
    mesa-gl

# Install build dependencies and then remove them
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    linux-headers \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Create non-root user
RUN adduser -D appuser
USER appuser

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]