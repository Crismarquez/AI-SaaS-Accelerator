FROM python:3.11-slim

WORKDIR /app

COPY ../../requirements /app/requirements
COPY requirements.txt /app/core/requirements.txt
RUN pip install --no-cache-dir -r /app/core/requirements.txt

COPY . /app/core/backend

ENV PYTHONPATH=/app

CMD ["uvicorn", "core.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]


