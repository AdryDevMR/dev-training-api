# User Tasks API

A FastAPI-based RESTful API for managing user accounts and tasks with strict HTTP status code handling.

## Features

- 🚀 FastAPI with Python 3.11
- 🐳 Docker and Docker Compose support
- 📝 OpenAPI documentation
- 📊 Structured logging with Loguru
- 🔒 JWT Authentication
- ✅ Input validation with Pydantic
- 🧪 100% test coverage
- 📦 Dependency management with Poetry

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Make (optional, but recommended)

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd dev-training-api
   ```

2. Copy the example environment file and update the values:
   ```bash
   cp .env.example .env
   ```

3. Start the development environment:
   ```bash
   docker-compose up --build
   ```

4. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Development

### Running Tests

```bash
docker-compose exec api pytest
```

### Code Style

We use `black`, `isort`, and `mypy` for code quality. Run them with:

```bash
docker-compose exec api black .
docker-compose exec api isort .
docker-compose exec api mypy .
```

### Database Migrations

We use Alembic for database migrations. To create a new migration:

```bash
docker-compose exec api alembic revision --autogenerate -m "Your migration message"
docker-compose exec api alembic upgrade head
```

## API Documentation

### Authentication

All endpoints except `/health` and `/token` require authentication. Include the JWT token in the `Authorization` header:

```
Authorization: Bearer <your-token>
```

### Response Format

All responses follow this format:

```json
{
  "success": true,
  "data": {
    // Response data
  }
}
```

For errors:

```json
{
  "success": false,
  "reason": "Error message"
}
```

## Deployment

### Production

1. Build the production image:
   ```bash
   docker build -t user-tasks-api .
   ```

2. Run the container:
   ```bash
   docker run -d --name user-tasks-api \
     -p 8000:8000 \
     --env-file .env \
     -v ./logs:/app/logs \
     user-tasks-api
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
