#!/bin/bash

DOCKER_NAME="audiodocker"
HOST_PORT=48080
CONTAINER_PORT=48080
SCRIPT_NAME="run_server.sh"
FOLDER_NAME="audioinfra"

# Запуск в интерактивном режиме с удалением контейнера после остановки
# Установка портов, монтирование директории, запуск скрипта
docker run\
            -it\
            --rm\
            -p $HOST_PORT:$CONTAINER_PORT\
            -v "$(pwd)/../..":/app\
            $DOCKER_NAME\
            -c "bash ./$FOLDER_NAME/$SCRIPT_NAME"