FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY agents ./agents
COPY evaluation ./evaluation
COPY orchestrator ./orchestrator
COPY pipelines ./pipelines
COPY prompts ./prompts
COPY providers ./providers
COPY service ./service
COPY vector_store ./vector_store
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e .

COPY . .

EXPOSE 8100
CMD ["uvicorn", "service.main:app", "--host", "0.0.0.0", "--port", "8100"]
