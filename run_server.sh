#!/bin/bash

UVICORN_PORT=48080
APP_NAME="server"
FOLDER_NAME="audioserver"

cd ./$FOLDER_NAME || exit
uvicorn $APP_NAME:app --host 0.0.0.0 --port $UVICORN_PORT
