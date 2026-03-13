#!/bin/bash

set -e

IMAGE="${DOCKER_USERNAME}/github-actions-capestone:latest"

echo "Pulling latest image..."
docker pull "$IMAGE"

echo "Starting container..."
docker run -d -p 5000:5000 --name app-test "$IMAGE"

echo "Waiting for container to start..."
sleep 5

echo "Running health check..."
curl --fail http://localhost:5000/health

echo "Health check passed"

echo "Stopping container..."
docker rm -f app-test
