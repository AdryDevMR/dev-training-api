# 🔧 Common Issues & Solutions

Troubleshooting guide for the most frequently encountered problems when running the User Account and Tasks API.

## 🚨 **Quick Diagnosis**

### **Check Application Status**
```bash
# Health check
curl http://localhost:8000/health

# Check if port is listening
lsof -i :8000

# Check Docker containers (if using Docker)
docker ps
docker-compose ps
```

### **Check Logs**
```bash
# Local logs
tail -f logs/app.log

# Docker logs
make docker-logs
# or
docker-compose logs -f api
```

## 🐳 **Docker Issues**

### **1. Container Won't Start**

#### **Problem**: Container exits immediately
```bash
# Check container logs
docker-compose logs api

# Check container status
docker ps -a
```

#### **Solutions**:
- **Port conflict**: Change port in `docker-compose.yml`
- **Permission issues**: Use `sudo` or add user to docker group
- **Missing dependencies**: Rebuild image with `make docker-build`

#### **Debug Commands**:
```bash
# Enter container interactively
docker run -it --rm dev-training-api /bin/bash

# Check container environment
docker exec -it dev-training-api env

# Test application manually
docker exec -it dev-training-api python start.py
```

### **2. Image Build Fails**

#### **Problem**: Docker build fails with errors
```bash
# Clean build (no cache)
docker build --no-cache -t dev-training-api .

# Check Dockerfile syntax
docker build --target builder -t dev-training-api .
```

#### **Common Build Issues**:
- **Python version mismatch**: Update Dockerfile base image
- **Dependency conflicts**: Check `requirements.txt` compatibility
- **System dependencies**: Ensure all required packages are in Dockerfile

### **3. Volume Mounting Issues**

#### **Problem**: Database or logs not persisting
```bash
# Check volume mounts
docker inspect dev-training-api | grep -A 10 Mounts

# Verify file permissions
ls -la logs/
ls -la app.db
```

#### **Solutions**:
- **Permission denied**: Check file ownership and permissions
- **Path issues**: Use absolute paths in docker-compose.yml
- **Missing directories**: Create directories before mounting

## 🏠 **Local Development Issues**

### **1. Port Already in Use**

#### **Problem**: `Address already in use` error
```bash
# Find process using port 8000
lsof -ti:8000

# Kill process
lsof -ti:8000 | xargs kill -9

# Alternative: Use different port
uvicorn app.main:app --reload --port 8001
```

#### **Common Port Conflicts**:
- **Jupyter Notebook**: Usually uses port 8888
- **Other FastAPI apps**: Check for multiple instances
- **Development servers**: Stop other running services

### **2. Python Dependencies Issues**

#### **Problem**: Import errors or missing packages
```bash
# Check Python version
python --version

# Verify virtual environment
which python
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### **Common Dependency Issues**:
- **Version conflicts**: Use virtual environment
- **Missing system packages**: Install development tools
- **Caching issues**: Clear pip cache with `pip cache purge`

### **3. Database Connection Issues**

#### **Problem**: Database errors or connection failures
```bash
# Check database file
ls -la app.db

# Check file permissions
ls -la app.db

# Verify SQLite installation
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

#### **Solutions**:
- **Permission denied**: Check directory write permissions
- **Corrupted database**: Delete `app.db` and restart
- **SQLite version**: Ensure Python has SQLite support

## 🔌 **API Issues**

### **1. Endpoints Not Responding**

#### **Problem**: API returns 404 or connection refused
```bash
# Test basic connectivity
curl http://localhost:8000/

# Test health endpoint
curl http://localhost:8000/health

# Check API routes
curl http://localhost:8000/docs
```

#### **Common Causes**:
- **Application not running**: Start the application
- **Wrong port**: Verify port configuration
- **Firewall blocking**: Check firewall settings
- **CORS issues**: Verify CORS configuration

### **2. Authentication Errors**

#### **Problem**: Password hashing or verification fails
```bash
# Check bcrypt installation
python -c "import bcrypt; print('bcrypt available')"

# Verify password hashing
python -c "from app.services.user_service import UserService; print('Service available')"
```

#### **Solutions**:
- **Missing bcrypt**: Install with `pip install bcrypt`
- **Version compatibility**: Update Python or bcrypt version
- **Import errors**: Check module structure and imports

### **3. Validation Errors**

#### **Problem**: Request validation fails
```bash
# Check request format
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{"action": "create", "data": {}}'
```

#### **Common Validation Issues**:
- **Missing required fields**: Check API documentation
- **Invalid data types**: Ensure proper JSON format
- **Field constraints**: Verify field lengths and formats

## 📊 **Performance Issues**

### **1. Slow Response Times**

#### **Problem**: API responses are slow
```bash
# Check response times
time curl http://localhost:8000/health

# Monitor resource usage
docker stats dev-training-api
# or
top -p $(pgrep -f "python start.py")
```

#### **Optimization Tips**:
- **Database indexing**: Add indexes for frequently queried fields
- **Connection pooling**: Optimize database connections
- **Caching**: Implement response caching
- **Resource limits**: Set appropriate Docker resource limits

### **2. High Memory Usage**

#### **Problem**: Application uses excessive memory
```bash
# Check memory usage
docker stats dev-training-api
# or
ps aux | grep python

# Monitor memory over time
watch -n 1 'docker stats --no-stream dev-training-api'
```

#### **Solutions**:
- **Memory leaks**: Check for unclosed connections or resources
- **Large datasets**: Implement pagination
- **Resource limits**: Set Docker memory limits
- **Garbage collection**: Monitor Python GC behavior

## 🗄️ **Database Issues**

### **1. SQLite Locking Issues**

#### **Problem**: Database locked errors
```bash
# Check for multiple processes
ps aux | grep python

# Check file locks
lsof app.db

# Verify single instance
netstat -tlnp | grep :8000
```

#### **Solutions**:
- **Single instance**: Ensure only one application instance
- **Connection pooling**: Optimize database connections
- **Transaction management**: Use proper transaction handling
- **File permissions**: Check database file permissions

### **2. Schema Migration Issues**

#### **Problem**: Database schema errors
```bash
# Check current schema
sqlite3 app.db ".schema"

# Verify models
python -c "from app.models import User, Task; print('Models loaded')"
```

#### **Solutions**:
- **Delete database**: Remove `app.db` and restart
- **Check migrations**: Verify model definitions
- **Version compatibility**: Ensure code and database compatibility

## 🔍 **Debugging Techniques**

### **1. Enable Debug Logging**

#### **Set Debug Level**:
```bash
# Environment variable
export LOG_LEVEL=DEBUG

# Or in .env file
LOG_LEVEL=DEBUG
```

#### **Debug Output**:
```bash
# View debug logs
tail -f logs/app.log | grep DEBUG

# Filter by specific component
tail -f logs/app.log | grep "app.api"
```

### **2. Interactive Debugging**

#### **Python Debugger**:
```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use Python 3.7+ breakpoint()
breakpoint()
```

#### **Docker Debugging**:
```bash
# Enter running container
docker exec -it dev-training-api /bin/bash

# Check application state
docker exec -it dev-training-api ps aux
docker exec -it dev-training-api netstat -tlnp
```

### **3. Network Debugging**

#### **Check Connectivity**:
```bash
# Test local connectivity
curl -v http://localhost:8000/health

# Check network interfaces
docker exec -it dev-training-api ip addr

# Test DNS resolution
docker exec -it dev-training-api nslookup google.com
```

## 🚀 **Prevention Tips**

### **1. Regular Maintenance**
- **Monitor logs** for errors and warnings
- **Check resource usage** regularly
- **Update dependencies** periodically
- **Backup database** regularly

### **2. Development Best Practices**
- **Use virtual environments** for Python development
- **Test changes** before deploying
- **Version control** all configuration changes
- **Document customizations** and modifications

### **3. Production Considerations**
- **Set resource limits** in Docker
- **Implement health checks** for monitoring
- **Use production Dockerfile** for live deployments
- **Configure proper logging** levels

## 🆘 **Getting More Help**

### **1. Check Documentation**
- **[API Documentation](http://localhost:8000/docs)** - Interactive API reference
- **[Installation Guide](../installation/README.md)** - Setup instructions
- **[Docker Guide](../deployment/docker.md)** - Container deployment

### **2. Common Commands Reference**
```bash
# Application management
make help              # Show all available commands
make run               # Run locally
make docker-run        # Run with Docker
make docker-logs       # View Docker logs
make clean             # Clean up files

# Docker management
docker ps              # List running containers
docker-compose ps      # List compose services
docker-compose logs    # View service logs
docker-compose down    # Stop services
```

### **3. External Resources**
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Docker Documentation**: https://docs.docker.com/
- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **Python Logging**: https://docs.python.org/3/library/logging.html

---

**Still stuck?** Check the logs for specific error messages, and don't hesitate to review the [installation guide](../installation/README.md) or [Docker deployment guide](../deployment/docker.md) for your specific setup.
