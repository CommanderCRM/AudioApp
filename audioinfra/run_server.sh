#!/bin/bash

UVICORN_PORT=48080
APP_NAME="server"
FOLDER_NAME="audioserver"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Переходим в папку с сервером и запускаем его локально
cd "$SCRIPT_DIR"/.. && cd $FOLDER_NAME || exit
uvicorn $APP_NAME:app --host 0.0.0.0 --port $UVICORN_PORT
