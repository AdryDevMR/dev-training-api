# User Account and Tasks API

A FastAPI-based API that manages user accounts and tasks with a simplified response system.

## Features

- **Simplified HTTP Status Codes**: Only returns 200 (success) or 500 (server error)
- **Action-Based Endpoints**: All endpoints accept POST requests with an "action" property
- **Supported Actions**: "edit", "create", "view"
- **Error Handling**: Errors return 200 status with error details in "reason" property
- **SQLite Database**: Lightweight database for development and testing
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Docker Support**: Full containerization with Docker and Docker Compose

## API Response Format

### Success Response (200)
```json
{
  "success": true,
  "data": {...}
}
```

### Error Response (200)
```json
{
  "success": false,
  "reason": "User-friendly error message"
}
```

### Server Error (500)
```json
{
  "success": false,
  "reason": "Internal server error"
}
```

## Endpoints

All endpoints accept POST requests with the following JSON structure:
```json
{
  "action": "create|edit|view",
  "data": {...}
}
```

### Available Endpoints:
- `/api/users` - User account management
- `/api/tasks` - Task management

## Installation & Running

### Option 1: Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python start.py
# or
make run
```

### Option 2: Docker (Recommended)

#### Quick Start with Docker Compose
```bash
# Build and run the application
make docker-run

# View logs
make docker-logs

# Stop the application
make docker-stop
```

#### Manual Docker Commands
```bash
# Build the image
docker build -t dev-training-api .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop containers
docker-compose down
```

#### Production Deployment
```bash
# Build and run production image
docker-compose -f docker-compose.prod.yml up -d

# Set environment variables
export SECRET_KEY="your-secure-secret-key"
docker-compose -f docker-compose.prod.yml up -d
```

## Available Make Commands

```bash
# Local Development
make install      # Install dependencies
make run         # Run locally
make test        # Run tests
make clean       # Clean up files
make logs        # View logs
make setup       # Setup directories

# Docker Commands
make docker-build   # Build Docker image
make docker-run     # Run with Docker Compose
make docker-stop    # Stop containers
make docker-logs    # View container logs
make docker-clean   # Clean up Docker resources

# Help
make help          # Show all commands
```

## Environment Variables

Create a `.env` file with:
```
DATABASE_URL=sqlite:///./app.db
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-here
```

## API Documentation

Once running, access the API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
dev-training-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── tasks.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── task_service.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── responses.py
├── logs/
├── requirements.txt
├── Dockerfile
├── Dockerfile.prod
├── docker-compose.yml
├── docker-compose.prod.yml
├── .dockerignore
├── Makefile
└── README.md
```

## Docker Features

- **Multi-stage builds** for optimized production images
- **Health checks** for container monitoring
- **Volume mounting** for persistent data and logs
- **Environment variable** configuration
- **Resource limits** for production deployments
- **Log rotation** and management
- **Non-root user** for security
