#!/bin/bash

source .env

echo $DOCKER_USERNAME
echo $SERVICE_NAME

docker build -t $DOCKER_USERNAME/$SERVICE_NAME .
docker push $DOCKER_USERNAME/$SERVICE_NAME:latest