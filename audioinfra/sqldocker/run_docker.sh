#!/bin/bash

DOCKER_NAME="sqldocker"
HOST_PORT=5432
CONTAINER_PORT=5432

# Запуск в интерактивном режиме с удалением контейнера после остановки
# Установка портов, монтирование директории
docker run\
            -it\
            --rm\
            -p $HOST_PORT:$CONTAINER_PORT\
            -v "$(pwd)/../..":/app\
            $DOCKER_NAME