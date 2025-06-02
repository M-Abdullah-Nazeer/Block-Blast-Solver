#!/bin/bash
docker compose down
docker rm -fv $(docker ps -aq) 2>/dev/null || true
docker rmi -f $(docker images -aq) 2>/dev/null || true
docker volume rm -f $(docker volume ls -q) 2>/dev/null || true
docker builder prune --all --force
git pull
docker compose up -d
