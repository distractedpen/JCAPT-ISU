#!/bin/bash

# build client and service images

docker build -t jcapt-client -f ../client.Dockerfile .

docker build -t jcapt-service -f ../service.Dockerfile .
