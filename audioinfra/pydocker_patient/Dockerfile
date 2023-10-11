# Первый этап - устанавливаем зависимости
FROM python:3.11-slim as builder
LABEL stage=intermediate

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir virtualenv==20.24.5 && virtualenv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Второй этап - копируем .venv из первого и подготавливаем к запуску
FROM python:3.11-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "uvicorn", "patient_server:app", "--host", "0.0.0.0", "--port", "50080"]