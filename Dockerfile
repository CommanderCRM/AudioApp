# Первый этап - устанавливаем зависимости
FROM python:3.10-slim as builder
LABEL stage=intermediate

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install virtualenv

RUN virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Второй этап - копируем .venv из первого и подготавливаем к запуску
FROM python:3.10-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT [ "/bin/bash" ]