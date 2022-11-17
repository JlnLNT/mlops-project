#! /bin/bash

aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 550501635282.dkr.ecr.eu-west-3.amazonaws.com

docker build -f Dockerfile_serverless -t windpower-prediction .

docker tag windpower-prediction:latest 550501635282.dkr.ecr.eu-west-3.amazonaws.com/windpower-prediction:latest

docker push 550501635282.dkr.ecr.eu-west-3.amazonaws.com/windpower-prediction:latest