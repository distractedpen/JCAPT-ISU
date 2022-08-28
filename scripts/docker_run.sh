#!/bin/bash

# Spin up both client and service dockers.

# client start
docker run -d --rm \
    --network jcapt-network \
    -p 40088:40088 \
    --name jcapt-client-container \
    jcapt-client

# service start
docker run --rm \
    --network jcapt-network \
    --env-file ../.env-service \
    -v /home/zach/projects/jcapt-isu/service/drills:/home/app/service/drills \
    -v /home/zach/projects/jcapt-isu/service/logs:/home/app/service/logs \
    -v /home/zach/projects/jcapt-isu/service/users:/home/app/service/users \
    --name jcapt-service-container \
    -p 40089:40089 \
    jcapt-service

