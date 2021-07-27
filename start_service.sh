#!/bin/bash

# build docker image
docker build -t motiontag_challenge .
# run docker image
docker container run -p 10400:10400 -it motiontag_challenge:latest

