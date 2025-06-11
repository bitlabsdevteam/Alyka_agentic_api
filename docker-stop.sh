#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed."
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

# Stop the containers
echo "Stopping the containers..."
docker-compose down

if [ $? -eq 0 ]; then
    echo "Containers stopped successfully!"
else
    echo "Error: Failed to stop containers."
    echo "Please check the logs for more information: docker-compose logs"
    exit 1
fi