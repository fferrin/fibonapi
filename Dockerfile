# Stage 1: Base image
FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

RUN pytest .

# ====================

# Stage 2: Production Stage
FROM python:3.11-slim

WORKDIR /app

COPY --from=build /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=build /app .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
