# 🐳 Docker Deployment Guide

Complete guide to deploying the User Account and Tasks API using Docker and Docker Compose.

## 📋 **Prerequisites**

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git** (for cloning the repository)

### **Install Docker**

#### **macOS**
```bash
# Install Docker Desktop
brew install --cask docker
# Or download from: https://www.docker.com/products/docker-desktop
```

#### **Ubuntu/Debian**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in for group changes to take effect
```

#### **Windows**
Download Docker Desktop from: https://www.docker.com/products/docker-desktop

## 🚀 **Quick Docker Deployment**

### **Step 1: Clone Repository**
```bash
git clone <repository-url>
cd dev-training-api
```

### **Step 2: Build and Run**
```bash
# Build the Docker image
make docker-build

# Run with Docker Compose
make docker-run
```

### **Step 3: Verify Deployment**
```bash
# Check container status
docker ps

# Test the API
curl http://localhost:8000/health

# View logs
make docker-logs
```

## 🔧 **Detailed Docker Commands**

### **Building the Image**
```bash
# Build with default tag
docker build -t dev-training-api .

# Build with specific tag
docker build -t dev-training-api:v1.0.0 .

# Build without cache (force rebuild)
docker build --no-cache -t dev-training-api .
```

### **Running with Docker Compose**
```bash
# Start in background
docker-compose up -d

# Start and view logs
docker-compose up

# Start specific service
docker-compose up -d api

# Scale services (if you add more)
docker-compose up -d --scale api=3
```

### **Managing Containers**
```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs api
docker-compose logs -f api  # Follow logs

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove everything (including volumes)
docker-compose down -v
```

## 🏭 **Production Docker Deployment**

### **Production Dockerfile**
The project includes a production-optimized Dockerfile (`Dockerfile.prod`) with:

- **Multi-stage builds** for smaller images
- **Security hardening** with non-root user
- **Resource optimization** for production workloads
- **Health checks** for monitoring

### **Production Deployment**
```bash
# Deploy production version
docker-compose -f docker-compose.prod.yml up -d

# Check production status
docker-compose -f docker-compose.prod.yml ps

# View production logs
docker-compose -f docker-compose.prod.yml logs -f api
```

### **Environment Configuration**
```bash
# Set production environment variables
export SECRET_KEY="your-secure-production-secret-key"
export LOG_LEVEL="WARNING"
export DATABASE_URL="sqlite:///./app.db"

# Deploy with environment variables
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 **Docker Configuration Options**

### **Port Configuration**
```yaml
# In docker-compose.yml
ports:
  - "8000:8000"        # Host:Container
  - "8080:8000"        # Change host port to 8080
  - "0.0.0.0:8000:8000" # Bind to all interfaces
```

### **Volume Mounting**
```yaml
# In docker-compose.yml
volumes:
  - ./logs:/app/logs           # Mount logs directory
  - ./app.db:/app/app.db       # Mount database file
  - ./config:/app/config       # Mount configuration
```

### **Environment Variables**
```yaml
# In docker-compose.yml
environment:
  - DATABASE_URL=sqlite:///./app.db
  - LOG_LEVEL=INFO
  - SECRET_KEY=your-secret-key
```

## 🔍 **Monitoring and Debugging**

### **Container Health Checks**
```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Health}}"

# View health check logs
docker inspect dev-training-api | grep -A 10 Health
```

### **Resource Usage**
```bash
# Monitor resource usage
docker stats dev-training-api

# View container details
docker inspect dev-training-api
```

### **Log Analysis**
```bash
# View recent logs
docker-compose logs --tail=100 api

# Search logs for errors
docker-compose logs api | grep ERROR

# Export logs to file
docker-compose logs api > api-logs.txt
```

## 🚨 **Troubleshooting Docker Issues**

### **Common Problems and Solutions**

| Issue | Solution |
|-------|----------|
| **Port already in use** | Change port in docker-compose.yml or stop conflicting service |
| **Permission denied** | Use `sudo` or add user to docker group |
| **Container won't start** | Check logs: `docker-compose logs api` |
| **Image build fails** | Check Dockerfile syntax and dependencies |
| **Database not persisting** | Verify volume mounts in docker-compose.yml |

### **Debug Commands**
```bash
# Enter running container
docker exec -it dev-training-api /bin/bash

# View container filesystem
docker exec -it dev-training-api ls -la

# Check environment variables
docker exec -it dev-training-api env

# Test network connectivity
docker exec -it dev-training-api curl localhost:8000/health
```

## 🔒 **Security Considerations**

### **Container Security**
- **Non-root user**: Application runs as `appuser`
- **Minimal base image**: Uses Python slim image
- **No unnecessary packages**: Only required dependencies installed
- **Health checks**: Monitors application health

### **Network Security**
```yaml
# Restrict network access
networks:
  default:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### **Resource Limits**
```yaml
# In docker-compose.prod.yml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
    reservations:
      cpus: '0.5'
      memory: 256M
```

## 📈 **Scaling and Performance**

### **Horizontal Scaling**
```bash
# Scale API service to multiple instances
docker-compose up -d --scale api=3

# Load balancer configuration (example with nginx)
# Add nginx service to docker-compose.yml
```

### **Performance Optimization**
- **Multi-stage builds** reduce image size
- **Layer caching** speeds up builds
- **Resource limits** prevent resource exhaustion
- **Health checks** ensure service availability

## 🔄 **Continuous Deployment**

### **Automated Builds**
```bash
# Build and push to registry
docker build -t your-registry/dev-training-api:latest .
docker push your-registry/dev-training-api:latest

# Pull and deploy
docker-compose pull
docker-compose up -d
```

### **CI/CD Integration**
```yaml
# Example GitHub Actions workflow
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy with Docker Compose
        run: |
          docker-compose -f docker-compose.prod.yml up -d
```

## 📚 **Next Steps**

After successful Docker deployment:

1. **[Configure Environment](environment.md)** - Set up production environment
2. **[Monitor Performance](troubleshooting/performance.md)** - Optimize your deployment
3. **[Set Up Logging](deployment/logging.md)** - Configure log aggregation
4. **[Backup Strategy](deployment/backup.md)** - Protect your data

## 🆘 **Need Help?**

- **Docker issues**: Check [troubleshooting section](../troubleshooting/common.md)
- **Performance problems**: Review [performance guide](../troubleshooting/performance.md)
- **Security concerns**: Consult [security best practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Happy Containerizing!** 🐳 Your API is now running in Docker with production-ready configuration.
