#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found."
    echo "Please copy .env.example to .env and add your API keys."
    echo "cp .env.example .env"
    exit 1
fi

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

# Build and start the containers
echo "Building and starting the containers..."
docker-compose up -d --build

# Check if the containers are running
if [ $? -eq 0 ]; then
    echo "Containers started successfully!"
    echo "API is now available at http://localhost:8000"
    echo "API documentation is available at http://localhost:8000/docs"
    echo ""
    echo "To view logs, run: docker-compose logs -f"
    echo "To stop the containers, run: docker-compose down"
else
    echo "Error: Failed to start containers."
    echo "Please check the logs for more information: docker-compose logs"
    exit 1
fi