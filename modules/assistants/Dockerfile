FROM python:3.11-slim

WORKDIR /app

COPY ../../requirements /app/requirements
COPY requirements.txt /app/modules/assistants/requirements.txt
RUN pip install --no-cache-dir -r /app/modules/assistants/requirements.txt

COPY . /app/modules/assistants

ENV PYTHONPATH=/app

CMD ["uvicorn", "modules.assistants.main:app", "--host", "0.0.0.0", "--port", "8000"]


