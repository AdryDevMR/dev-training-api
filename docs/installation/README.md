# 🚀 Installation Guide

This guide covers all the ways to install and run the User Account and Tasks API.

## 📋 **Prerequisites**

Before you begin, ensure you have the following installed:

- **Python 3.8+** (3.11+ recommended)
- **pip** (Python package installer)
- **Git** (for cloning the repository)

### **System Requirements**

- **Memory**: Minimum 512MB RAM
- **Storage**: At least 100MB free space
- **Network**: Internet access for downloading dependencies

## 🎯 **Installation Options**

Choose the installation method that best fits your needs:

| Method | Use Case | Difficulty | Time |
|--------|----------|------------|------|
| **[Local Installation](#local-installation)** | Development, Testing | Easy | 5-10 minutes |
| **[Docker Installation](#docker-installation)** | Production, Deployment | Medium | 3-5 minutes |
| **[Production Installation](#production-installation)** | Live Systems | Advanced | 10-15 minutes |

## 🏠 **Local Installation**

### **Step 1: Clone the Repository**

```bash
git clone <repository-url>
cd dev-training-api
```

### **Step 2: Create Virtual Environment (Recommended)**

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

### **Step 4: Set Up Environment**

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your configuration
# (Optional: Modify database URL, log level, etc.)
```

### **Step 5: Run the Application**

```bash
# Option 1: Direct execution
python start.py

# Option 2: Using Makefile
make run

# Option 3: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Step 6: Verify Installation**

Open your browser and navigate to:
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Documentation**: http://localhost:8000/docs

## 🐳 **Docker Installation**

### **Prerequisites for Docker**

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)

### **Step 1: Clone and Navigate**

```bash
git clone <repository-url>
cd dev-training-api
```

### **Step 2: Build and Run**

```bash
# Option 1: Using Makefile (Recommended)
make docker-run

# Option 2: Manual Docker commands
docker-compose up -d
```

### **Step 3: Verify Installation**

```bash
# Check container status
docker ps

# View logs
make docker-logs
# or
docker-compose logs -f api

# Test the API
curl http://localhost:8000/health
```

### **Step 4: Access the Application**

- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs

## 🏭 **Production Installation**

### **Prerequisites for Production**

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Environment variables** configured
- **SSL certificates** (if using HTTPS)

### **Step 1: Configure Environment**

```bash
# Set production environment variables
export SECRET_KEY="your-secure-production-secret-key"
export LOG_LEVEL="WARNING"
export DATABASE_URL="sqlite:///./app.db"
```

### **Step 2: Deploy with Production Compose**

```bash
# Deploy production version
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

### **Step 3: Monitor and Maintain**

```bash
# View production logs
docker-compose -f docker-compose.prod.yml logs -f api

# Check health
curl http://localhost:8000/health
```

## 🔧 **Post-Installation Setup**

### **Create Initial Data (Optional)**

```bash
# Run the test script to create sample data
python test_api.py
```

### **Configure Logging**

Logs are automatically created in the `logs/` directory. You can:

- **View logs**: `make logs` or `tail -f logs/app.log`
- **Configure log level**: Set `LOG_LEVEL` in your `.env` file
- **Log rotation**: Logs automatically rotate when they reach 10MB

### **Database Management**

The SQLite database (`app.db`) is automatically created on first run. You can:

- **Backup**: Copy `app.db` to a safe location
- **Reset**: Delete `app.db` to start fresh
- **Migrate**: The database schema is automatically managed

## ✅ **Verification Checklist**

After installation, verify these items:

- [ ] Application starts without errors
- [ ] Health endpoint responds: `curl http://localhost:8000/health`
- [ ] API documentation is accessible: http://localhost:8000/docs
- [ ] Logs are being generated in `logs/` directory
- [ ] Database file `app.db` is created
- [ ] Can create a test user via API

## 🚨 **Common Installation Issues**

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Change port in `start.py` or stop other services |
| Permission denied | Check file permissions or use `sudo` (Docker) |
| Dependencies fail to install | Update pip: `pip install --upgrade pip` |
| Database errors | Ensure write permissions in project directory |

## 📚 **Next Steps**

After successful installation:

1. **[Read the API Overview](api/overview.md)** to understand the API structure
2. **[Try Basic Examples](examples/basic.md)** to test functionality
3. **[Configure Environment](deployment/environment.md)** for your needs
4. **[Deploy to Production](deployment/production.md)** when ready

## 🆘 **Need Help?**

If you encounter issues during installation:

1. Check the [troubleshooting section](../troubleshooting/common.md)
2. Review the [common issues](../troubleshooting/common.md)
3. Ensure all prerequisites are met
4. Check the logs for error messages

---

**Congratulations!** 🎉 You've successfully installed the User Account and Tasks API. Now explore the [API documentation](api/overview.md) to start using it!
