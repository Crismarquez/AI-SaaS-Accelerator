FROM python:3.11-slim

WORKDIR /app

COPY ../../requirements /app/requirements
COPY requirements.txt /app/modules/payments/requirements.txt
RUN pip install --no-cache-dir -r /app/modules/payments/requirements.txt

COPY . /app/modules/payments

ENV PYTHONPATH=/app

CMD ["uvicorn", "modules.payments.main:app", "--host", "0.0.0.0", "--port", "8000"]


