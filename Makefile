.PHONY: install run test clean logs help docker-build docker-run docker-stop docker-logs docker-clean

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "Local Development:"
	@echo "  install    - Install dependencies"
	@echo "  run        - Run the FastAPI application"
	@echo "  test       - Run the test script"
	@echo "  clean      - Clean up generated files"
	@echo "  logs       - View application logs"
	@echo "  setup      - Setup project directories"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run with Docker Compose"
	@echo "  docker-stop   - Stop Docker containers"
	@echo "  docker-logs   - View Docker container logs"
	@echo "  docker-clean  - Clean up Docker resources"
	@echo ""
	@echo "  help       - Show this help message"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run the application
run:
	@echo "Starting FastAPI application..."
	python start.py

# Run tests
test:
	@echo "Running API tests..."
	python test_api.py

# Clean up
clean:
	@echo "Cleaning up..."
	rm -f app.db
	rm -f app.db-journal
	rm -rf logs/*.log
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf app/*/__pycache__

# View logs
logs:
	@echo "Viewing application logs..."
	tail -f logs/app.log

# Create logs directory
setup:
	@echo "Setting up project..."
	mkdir -p logs
	@echo "Project setup complete!"

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t dev-training-api .

docker-run:
	@echo "Starting application with Docker Compose..."
	docker-compose up -d

docker-stop:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "Viewing Docker container logs..."
	docker-compose logs -f api

docker-clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v --remove-orphans
	docker image rm dev-training-api
	docker system prune -f
