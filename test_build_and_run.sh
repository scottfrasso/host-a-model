#!/bin/bash


docker build --no-cache -f server/Dockerfile -t api-server:latest ./server/

#docker run -d --name my-api-server -p 8081:8080 api-server:latest


#docker run --name my-api-server -p 8081:8080 api-server:latest

docker run --name my-api-server -p 8081:8080 api-server:latest ai_worker_api:app --host 0.0.0.0 --port 8080