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


# renew ssl
# sudo docker stop block-blast-solver-nginx-1
# 1. Check current certificates
# sudo certbot certificates

# 2. Delete duplicates below is example
# sudo certbot delete --cert-name blockblastsolverai.com-0001
# sudo certbot delete --cert-name blockblastsolverai.com

# 3. Get fresh certificate
# sudo certbot certonly --standalone -d blockblastsolverai.com -d www.blockblastsolverai.com --non-interactive --agree-tos

# 4. Start Docker nginx
# sudo docker start block-blast-solver-nginx-1