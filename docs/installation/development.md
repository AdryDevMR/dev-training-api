# 🏠 Development Setup Guide

Complete guide for setting up a local development environment for the User Account and Tasks API.

## 📋 **Prerequisites**

- **Python 3.8+** (3.11+ recommended)
- **Git** for version control
- **pip** for package management
- **Virtual environment** (recommended)

## 🚀 **Quick Development Setup**

### **Step 1: Clone Repository**
```bash
git clone <repository-url>
cd dev-training-api
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Run Development Server**
```bash
# Option 1: Using Makefile
make run

# Option 2: Direct execution
python start.py

# Option 3: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 **Development Configuration**

### **Environment Variables**
Create a `.env` file in the project root:
```bash
# Copy environment template
cp env.example .env

# Edit with your preferences
nano .env
```

**Recommended Development Settings**:
```bash
# Database
DATABASE_URL=sqlite:///./app.db

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log

# Security (use different keys for development)
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_PREFIX=/api
TITLE=User Account and Tasks API (Dev)
VERSION=1.0.0
DESCRIPTION=Development API for managing user accounts and tasks
```

### **Database Configuration**
The development setup uses SQLite by default:
- **File**: `app.db` (created automatically)
- **Location**: Project root directory
- **Backup**: Copy `app.db` before major changes
- **Reset**: Delete `app.db` to start fresh

## 🧪 **Development Workflow**

### **1. Code Changes**
```bash
# Make your code changes
# The server will auto-reload (if using --reload flag)

# Check for syntax errors
python -m py_compile app/main.py

# Run linting (if configured)
# flake8 app/
# black app/
```

### **2. Testing Changes**
```bash
# Test the API
python test_api.py

# Manual testing with curl
curl http://localhost:8000/health

# Check API documentation
open http://localhost:8000/docs
```

### **3. Database Changes**
```bash
# If you modify models, restart the application
# The database schema will be automatically updated

# View current schema
sqlite3 app.db ".schema"

# Reset database (if needed)
rm app.db
# Restart application
```

## 📊 **Development Tools**

### **Available Make Commands**
```bash
# View all commands
make help

# Development commands
make run          # Run development server
make test         # Run test script
make clean        # Clean up generated files
make logs         # View application logs
make setup        # Setup project directories
```

### **Logging During Development**
```bash
# View real-time logs
make logs

# Filter logs by level
tail -f logs/app.log | grep DEBUG
tail -f logs/app.log | grep ERROR

# Search logs
grep "User created" logs/app.log
```

### **Database Management**
```bash
# View database contents
sqlite3 app.db "SELECT * FROM users;"
sqlite3 app.db "SELECT * FROM tasks;"

# Export database
sqlite3 app.db ".dump" > backup.sql

# Import database
sqlite3 app.db < backup.sql
```

## 🔍 **Debugging Development Issues**

### **Common Development Problems**

#### **1. Import Errors**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Verify virtual environment
which python
pip list

# Check module structure
python -c "from app.main import app; print('App loaded')"
```

#### **2. Database Connection Issues**
```bash
# Check database file
ls -la app.db

# Test SQLite
python -c "import sqlite3; print('SQLite available')"

# Check permissions
ls -la app.db
```

#### **3. Port Conflicts**
```bash
# Check what's using port 8000
lsof -i :8000

# Use different port
uvicorn app.main:app --reload --port 8001
```

### **Debug Mode**
Enable debug logging for development:
```bash
# Set debug level
export LOG_LEVEL=DEBUG

# Or in .env file
LOG_LEVEL=DEBUG
```

## 🚀 **Development Best Practices**

### **1. Code Organization**
- **Keep models simple** and focused
- **Use services** for business logic
- **Validate inputs** with Pydantic schemas
- **Handle errors gracefully** with proper logging

### **2. Testing Strategy**
- **Test API endpoints** with real HTTP requests
- **Verify error handling** for edge cases
- **Check response formats** for consistency
- **Test database operations** with sample data

### **3. Performance Considerations**
- **Use pagination** for large datasets
- **Implement efficient queries** with proper indexing
- **Monitor memory usage** during development
- **Profile slow operations** with timing logs

## 🔄 **Development vs Production**

### **Key Differences**

| Aspect | Development | Production |
|--------|-------------|------------|
| **Log Level** | DEBUG | WARNING/ERROR |
| **Auto-reload** | Enabled | Disabled |
| **Debug Info** | Full | Minimal |
| **Error Details** | Detailed | Sanitized |
| **Database** | SQLite | SQLite/PostgreSQL |

### **Environment-Specific Configs**
```python
# In your code
if settings.environment == "development":
    # Development-specific behavior
    app.debug = True
    app.reload = True
else:
    # Production behavior
    app.debug = False
    app.reload = False
```

## 📚 **Development Resources**

### **Local Documentation**
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### **Useful Development Commands**
```bash
# Quick health check
curl -s http://localhost:8000/health | jq .

# Test user creation
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{"action":"create","data":{"username":"test","email":"test@test.com","full_name":"Test User","password":"password123"}}'

# View recent logs
tail -n 50 logs/app.log

# Check database size
du -h app.db
```

### **Development Scripts**
Create custom scripts for common development tasks:
```bash
#!/bin/bash
# dev-setup.sh
echo "Setting up development environment..."
cp env.example .env
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p logs
echo "Development environment ready!"
```

## 🆘 **Getting Help**

### **Development Issues**
- **Check logs**: `make logs` or `tail -f logs/app.log`
- **Verify setup**: Run `make setup` to ensure directories exist
- **Test connectivity**: Use `curl http://localhost:8000/health`
- **Check dependencies**: Verify `pip list` output

### **Common Development Questions**
- **Q**: Why isn't my code reloading?
  **A**: Ensure you're using `--reload` flag or `make run`
- **Q**: How do I reset the database?
  **A**: Delete `app.db` and restart the application
- **Q**: Where are the logs?
  **A**: Check `logs/app.log` or run `make logs`

---

**Happy Developing!** 🚀 Your local development environment is now ready. Make changes, test them, and watch the API evolve!
