# Makefile for Agentic API Project

# Variables
PYTHON = python3
PIP = pip3
APP_NAME = agentic_api
API_PORT ?= 8000

# Docker commands
DOCKER_COMPOSE = docker compose

# Colors for terminal output
GREEN = \033[0;32m
YELLOW = \033[0;33m
NC = \033[0m # No Color

.PHONY: help setup install run test clean docker-build docker-run docker-stop docker-logs lint format all

# Default target
all: help

# Help target
help:
	@echo "${GREEN}Agentic API Makefile${NC}"
	@echo "${YELLOW}Available targets:${NC}"
	@echo "  ${YELLOW}setup${NC}         - Create virtual environment and install dependencies"
	@echo "  ${YELLOW}install${NC}       - Install dependencies"
	@echo "  ${YELLOW}run${NC}           - Run the API server locally"
	@echo "  ${YELLOW}test${NC}          - Run the simple test"
	@echo "  ${YELLOW}docker-build${NC}  - Build the Docker image"
	@echo "  ${YELLOW}docker-run${NC}    - Run the application in Docker"
	@echo "  ${YELLOW}docker-stop${NC}   - Stop Docker containers"
	@echo "  ${YELLOW}docker-logs${NC}   - View Docker container logs"
	@echo "  ${YELLOW}clean${NC}         - Clean up generated files"
	@echo "  ${YELLOW}lint${NC}          - Run linting checks"
	@echo "  ${YELLOW}format${NC}        - Format code using black"

# Setup virtual environment and install dependencies
setup:
	@echo "${GREEN}Setting up virtual environment...${NC}"
	${PYTHON} -m venv venv
	@echo "${GREEN}Installing dependencies...${NC}"
	. venv/bin/activate && ${PIP} install -r requirements.txt
	@echo "${GREEN}Setup complete. Activate the virtual environment with:${NC}"
	@echo "source venv/bin/activate"

# Install dependencies
install:
	@echo "${GREEN}Installing dependencies...${NC}"
	${PIP} install -r requirements.txt

# Run the API server
run:
	@echo "${GREEN}Starting API server on port ${API_PORT}...${NC}"
	${PYTHON} server.py

# Run the simple test
test:
	@echo "${GREEN}Running simple test...${NC}"
	${PYTHON} simple_test.py

# Docker build
docker-build:
	@echo "${GREEN}Building Docker image...${NC}"
	${DOCKER_COMPOSE} build

# Docker run
docker-run:
	@echo "${GREEN}Starting Docker containers...${NC}"
	./docker-run.sh

# Docker stop
docker-stop:
	@echo "${GREEN}Stopping Docker containers...${NC}"
	./docker-stop.sh

# Docker logs
docker-logs:
	@echo "${GREEN}Viewing Docker logs...${NC}"
	${DOCKER_COMPOSE} logs -f

# Clean up generated files
clean:
	@echo "${GREEN}Cleaning up...${NC}"
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +

# Linting
lint:
	@echo "${GREEN}Running linting checks...${NC}"
	@if command -v flake8 > /dev/null; then \
		flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; \
	else \
		echo "${YELLOW}flake8 not installed. Run 'pip install flake8' to install.${NC}"; \
	fi

# Format code
format:
	@echo "${GREEN}Formatting code...${NC}"
	@if command -v black > /dev/null; then \
		black .; \
	else \
		echo "${YELLOW}black not installed. Run 'pip install black' to install.${NC}"; \
	fi