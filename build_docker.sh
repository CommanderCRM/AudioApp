#!/bin/bash

DOCKER_NAME="audiodocker"

docker build -t $DOCKER_NAME .

# удаление промежуточного образа
docker rmi -f "$(docker images -q --filter label=stage=intermediate)"
