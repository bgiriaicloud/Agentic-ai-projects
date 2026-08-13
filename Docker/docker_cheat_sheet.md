# Docker CLI Command Cheat Sheet

This document compiles the essential Docker commands and flags used in daily container management, image construction, and system troubleshooting.

---

## 📋 Table of Contents
1.  [Container Lifecycle Management](#1-container-lifecycle-management)
2.  [Docker Image Administration](#2-docker-image-administration)
3.  [Container Diagnostics, Inspection & Logs](#3-container-diagnostics-inspection--logs)
4.  [Volume & Storage Configuration](#4-volume--storage-configuration)
5.  [Network Configuration](#5-network-configuration)
6.  [System Cleanup & Pruning](#6-system-cleanup--pruning)

---

## 1. Container Lifecycle Management

```bash
# Create and start a container from an image in the background (detached mode)
docker run -d --name my-web-app -p 8080:80 nginx:latest

# Run an interactive container with standard input and a pseudo-TTY attached
docker run -it --name alpine-shell alpine:latest /bin/sh

# Run a container and automatically remove it when it exits
docker run --rm -it python:3.11-slim python -c "print('Hello')"

# Start one or more stopped containers
docker start my-web-app

# Stop a running container gracefully (sends SIGTERM, then SIGKILL after grace period)
docker stop my-web-app

# Restart a container gracefully
docker restart my-web-app

# Kill a running container immediately (sends SIGKILL)
docker kill my-web-app

# Remove a stopped container
docker rm my-web-app

# Force remove a running container (sends SIGKILL, then deletes container)
docker rm -f my-web-app
```

---

## 2. Docker Image Administration

```bash
# Build an image from a Dockerfile in the current directory
docker build -t my-app:v1.0 .

# Build an image bypassing the local layer cache (forces fresh packages download)
docker build --no-cache -t my-app:v1.0 .

# List all locally cached images
docker images

# Tag an existing image to a new repository or version name
docker tag my-app:v1.0 myregistry.com/org/my-app:latest

# Download an image from Docker Hub or a private registry
docker pull python:3.11-slim

# Push a tagged image to a registry
docker push myregistry.com/org/my-app:latest

# Remove a local image from the cache
docker rmi my-app:v1.0

# Export an image to a tar archive file (offline distribution)
docker save -o my-image.tar my-app:v1.0

# Load an image from a tar archive file
docker load -i my-image.tar
```

---

## 3. Container Diagnostics, Inspection & Logs

```bash
# List only running containers
docker ps

# List all containers (including stopped, exited, or crashed instances)
docker ps -a

# Stream a container's stdout and stderr logs in real-time
docker logs -f my-web-app

# View only the last 100 log lines with timestamp tags
docker logs --tail 100 -t my-web-app

# Open an interactive shell inside a running container (exec)
docker exec -it my-web-app /bin/bash

# View detailed JSON metadata of a container or image (network, mounts, variables)
docker inspect my-web-app

# Display the active processes running inside a container
docker top my-web-app

# View real-time resource usage statistics (CPU, memory, net/disk I/O)
docker stats

# Copy files or folders between a container and the local filesystem
docker cp my-web-app:/var/log/nginx/error.log ./local-logs/
```

---

## 4. Volume & Storage Configuration

Manage persistent storage volumes separate from container lifecycles.

```bash
# List all active Docker volumes
docker volume ls

# Create a new named volume
docker volume create app-data

# Display detailed JSON metadata of a volume (mount point on host disk)
docker volume inspect app-data

# Delete a volume
docker volume rm app-data

# Delete all unused local volumes (reclaims host disk space)
docker volume prune
```

---

## 5. Network Configuration

Manage container-to-container communication and port exposure.

```bash
# List all networks on the Docker host
docker network ls

# Create a user-defined bridge network (supports automatic DNS resolution between containers)
docker network create my-bridge-net

# Connect a running container to a network
docker network connect my-bridge-net my-web-app

# Disconnect a container from a network
docker network disconnect my-bridge-net my-web-app

# Delete a network
docker network rm my-bridge-net
```

---

## 6. System Cleanup & Pruning

Reclaim host memory, storage, and networking resources.

```bash
# Remove stopped containers, unused networks, and dangling images
docker system prune

# Deep cleanup: removes all stopped containers, unused networks, unused volumes, and all images without active containers
docker system prune -a --volumes
```
