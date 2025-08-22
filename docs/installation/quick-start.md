# ⚡ Quick Start Guide

Get the User Account and Tasks API running in **5 minutes** or less!

## 🎯 **Choose Your Path**

| I want to... | Follow this path |
|--------------|------------------|
| **Try it quickly** | [Docker Quick Start](#docker-quick-start) ⭐ |
| **Develop locally** | [Local Quick Start](#local-quick-start) |
| **Deploy to production** | [Production Quick Start](#production-quick-start) |

## 🐳 **Docker Quick Start (Recommended)**

### **Step 1: Clone & Navigate**
```bash
git clone <repository-url>
cd dev-training-api
```

### **Step 2: Run with One Command**
```bash
make docker-run
```

### **Step 3: Test It Works**
```bash
curl http://localhost:8000/health
```

### **Step 4: Open API Docs**
Open your browser to: **http://localhost:8000/docs**

🎉 **That's it!** Your API is running.

---

## 🏠 **Local Quick Start**

### **Step 1: Clone & Navigate**
```bash
git clone <repository-url>
cd dev-training-api
```

### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 3: Run the App**
```bash
python start.py
```

### **Step 4: Test It Works**
Open: **http://localhost:8000/docs**

---

## 🏭 **Production Quick Start**

### **Step 1: Clone & Navigate**
```bash
git clone <repository-url>
cd dev-training-api
```

### **Step 2: Set Environment**
```bash
export SECRET_KEY="your-secure-key-here"
```

### **Step 3: Deploy**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### **Step 4: Verify**
```bash
curl http://localhost:8000/health
```

---

## 🧪 **Quick Test**

Once running, test the API with this simple example:

```bash
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

## 🚨 **Common Quick Issues**

| Problem | Quick Fix |
|---------|-----------|
| Port 8000 busy | `lsof -ti:8000 | xargs kill -9` |
| Docker not running | Start Docker Desktop |
| Permission denied | `sudo make docker-run` |

## 📚 **What's Next?**

After quick start:
- **[Full Installation Guide](README.md)** - Complete setup details
- **[API Examples](examples/basic.md)** - Learn to use the API
- **[Docker Guide](deployment/docker.md)** - Master containerization

---

**Need help?** Check the [troubleshooting section](../troubleshooting/common.md) or run `make help` for all available commands.
