#!/bin/bash

echo "Setup started"
sudo apt update

curl -fsSL https://get.docker.com | sh
sudo apt-get install docker-compose-plugin

sudo docker compose version
