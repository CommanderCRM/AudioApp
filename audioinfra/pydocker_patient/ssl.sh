#!/bin/bash

# Данные для выпуска сертификата
SUBJECT="/C=RU/ST=Tomskaya oblast/L=Tomsk/O=TUSUR/OU=KIBEVS/CN=Tusuraudio"

# Выпуск сертификата
mkdir -p /usr/share
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out /usr/share/cert.key
openssl req -new -x509 -days 365 -key /usr/share/cert.key -out /usr/share/cert.cer \
  -subj "$SUBJECT"
