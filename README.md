# User Account and Tasks API

A FastAPI-based API that manages user accounts and tasks with a simplified response system.

## 🚀 **Quick Start**

### **Get Running in 5 Minutes**
```bash
# Clone and navigate
git clone <repository-url>
cd dev-training-api

# Run with Docker (Recommended)
make docker-run

# Test it works
curl http://localhost:8000/health

# Open API docs
open http://localhost:8000/docs
```

🎉 **That's it!** Your API is running at http://localhost:8000

## 📚 **📖 Comprehensive Documentation**

**New!** Complete documentation is now available in the `docs/` directory:

- **[🚀 Quick Start](docs/installation/quick-start.md)** - Get running in 5 minutes
- **[🏠 Development Setup](docs/installation/development.md)** - Local development environment  
- **[🐳 Docker Deployment](docs/deployment/docker.md)** - Container deployment guide
- **[🔌 API Overview](docs/api/overview.md)** - Architecture and design
- **[💡 Basic Examples](docs/examples/basic.md)** - Usage examples and tutorials
- **[🔧 Troubleshooting](docs/troubleshooting/common.md)** - Common issues and solutions

**[📚 View All Documentation](docs/README.md)** | **[📋 Documentation Overview](docs/DOCUMENTATION_OVERVIEW.md)**

## ✨ **Features**

- **Simplified HTTP Status Codes**: Only returns 200 (success/error) or 500 (server error)
- **Action-Based Endpoints**: All endpoints accept POST requests with an "action" property
- **Supported Actions**: "edit", "create", "view"
- **Error Handling**: Errors return 200 status with error details in "reason" property
- **SQLite Database**: Lightweight database for development and testing
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **🐳 Docker Support**: Full containerization with Docker and Docker Compose

## 🔄 **API Response Format**

### **Success Response (200)**
```json
{
  "success": true,
  "data": {...}
}
```

### **Error Response (200)**
```json
{
  "success": false,
  "reason": "User-friendly error message"
}
```

### **Server Error (500)**
```json
{
  "success": false,
  "reason": "Internal server error"
}
```

## 🛣️ **Endpoints**

All endpoints accept POST requests with the following JSON structure:
```json
{
  "action": "create|edit|view",
  "data": {...}
}
```

### **Available Endpoints:**
- `/api/users` - User account management
- `/api/tasks` - Task management

## 🚀 **Installation Options**

### **Option 1: Docker (Recommended)**
```bash
# Quick start
make docker-run

# Manual Docker
docker-compose up -d
```

### **Option 2: Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
make run
# or
python start.py
```

### **Option 3: Production**
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

## 🛠️ **Available Commands**

```bash
# View all commands
make help

# Docker commands
make docker-build   # Build Docker image
make docker-run     # Run with Docker Compose
make docker-stop    # Stop containers
make docker-logs    # View container logs

# Local development
make run            # Run locally
make test           # Run tests
make clean          # Clean up files
make logs           # View logs
```

## 🔧 **Environment Variables**

Create a `.env` file with:
```bash
DATABASE_URL=sqlite:///./app.db
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-change-in-production
```

## 📊 **Project Structure**

```
dev-training-api/
├── app/                    # Application code
│   ├── main.py            # FastAPI application
│   ├── config.py          # Configuration management
│   ├── database.py        # Database setup
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── api/               # API endpoints
│   ├── services/          # Business logic
│   └── utils/             # Utilities
├── docs/                   # 📚 Comprehensive documentation
├── logs/                   # Application logs
├── requirements.txt        # Python dependencies
├── Dockerfile              # Development container
├── Dockerfile.prod         # Production container
├── docker-compose.yml      # Development orchestration
├── docker-compose.prod.yml # Production orchestration
├── Makefile                # Development commands
└── README.md               # This file
```

## 🧪 **Testing**

### **Run Test Script**
```bash
python test_api.py
```

### **Manual Testing**
```bash
# Health check
curl http://localhost:8000/health

# Create a test user
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create",
    "data": {
      "username": "testuser",
      "email": "test@example.com",
      "full_name": "Test User",
      "password": "password123"
    }
  }'
```

## 📖 **API Documentation**

Once running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 **Docker Features**

- **Multi-stage builds** for optimized production images
- **Health checks** for container monitoring
- **Volume mounting** for persistent data and logs
- **Environment variable** configuration
- **Resource limits** for production deployments
- **Log rotation** and management
- **Security** with non-root user

## 🆘 **Need Help?**

### **📚 Documentation**
- **[Quick Start Guide](docs/installation/quick-start.md)** - Get running in 5 minutes
- **[Complete Installation](docs/installation/README.md)** - Full setup instructions
- **[Troubleshooting](docs/troubleshooting/common.md)** - Common issues and solutions

### **🔧 Commands**
- **View all commands**: `make help`
- **Check logs**: `make logs` or `make docker-logs`
- **Health check**: `curl http://localhost:8000/health`

### **🐛 Common Issues**
- **Port 8000 busy**: `lsof -ti:8000 | xargs kill -9`
- **Docker issues**: Check [Docker troubleshooting](docs/troubleshooting/common.md#docker-issues)
- **API not responding**: Verify application is running and check logs

## 🤝 **Contributing**

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

## 📄 **License**

This project is open source and available under the [MIT License](LICENSE).

---

**🎉 Ready to get started?** 

- **Quick start**: Follow the [5-minute guide](docs/installation/quick-start.md)
- **Full setup**: Read the [complete installation guide](docs/installation/README.md)
- **Learn the API**: Check the [examples and tutorials](docs/examples/basic.md)
- **Need help?**: Review the [troubleshooting guide](docs/troubleshooting/common.md)

**Happy coding!** 🚀
