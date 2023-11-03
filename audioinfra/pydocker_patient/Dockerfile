# Первый этап - устанавливаем зависимости
FROM python:3.11-slim as builder
LABEL stage=intermediate

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir virtualenv==20.24.5 && virtualenv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
COPY install_pygost.sh .
COPY ssl.sh .
RUN apt-get update && apt-get -y install wget=1.21.3-1+b2 --no-install-recommends \
&& apt-get -y install zstd=1.5.4+dfsg2-5 --no-install-recommends \
&& apt-get -y install openssl=3.0.11-1~deb12u2 --no-install-recommends \
&& pip install --no-cache-dir -r requirements.txt \
&& ./install_pygost.sh \
&& ./ssl.sh

# Второй этап - копируем .venv из первого и подготавливаем к запуску
FROM python:3.11-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY --from=builder /usr/share/cert.key /usr/share
COPY --from=builder /usr/share/cert.cer /usr/share

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "uvicorn", "patient_server:app", "--host", "0.0.0.0", "--port", "50080",\
            "--ssl-certfile", "/usr/share/cert.cer", "--ssl-keyfile", "/usr/share/cert.key"]