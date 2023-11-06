#!/bin/bash

docker build -f server/Dockerfile -t europe-central2-docker.pkg.dev/host-a-model/host-a-model-repo/api --no-cache --platform linux/amd64 ./server/

docker push europe-central2-docker.pkg.dev/host-a-model/host-a-model-repo/api
