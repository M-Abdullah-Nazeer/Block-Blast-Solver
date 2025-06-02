# Force-stop and remove all containers (including running ones)
docker rm -fv $(docker ps -aq) 2>/dev/null || true
# Remove all images (including dangling and tagged images)
docker rmi -f $(docker images -aq) 2>/dev/null || true
# Delete all volumes (irreversible data loss!)
docker volume rm -f $(docker volume ls -q) 2>/dev/null || true
# Prune build cache (from Docker BuildKit)
docker builder prune --all --force

chmod +x reset-docker.sh
./reset-docker.sh