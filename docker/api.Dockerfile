FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml README.md ./
COPY config ./config
COPY src ./src
COPY scripts ./scripts
COPY alembic.ini ./
RUN pip install --no-cache-dir .
RUN mkdir -p uploads
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
