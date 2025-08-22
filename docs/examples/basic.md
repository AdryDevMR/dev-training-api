# 💡 Basic Examples

Learn how to use the User Account and Tasks API with practical examples for common use cases.

## 🎯 **Getting Started**

### **Base URL**
```
http://localhost:8000/api
```

### **Request Format**
All API requests follow this structure:
```json
{
  "action": "create|edit|view",
  "data": {
    // Action-specific data
  }
}
```

## 👥 **User Management Examples**

### **1. Create a New User**

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create",
    "data": {
      "username": "john_doe",
      "email": "john@example.com",
      "full_name": "John Doe",
      "password": "securepassword123",
      "is_active": true,
      "is_admin": false
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

### **2. View a Specific User**

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "id": 1
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": null
  }
}
```

### **3. View User by Username**

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "username": "john_doe"
    }
  }'
```

### **4. View All Users with Pagination**

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "page": 1,
      "size": 10
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": {
    "users": [
      {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "is_active": true,
        "is_admin": false,
        "created_at": "2024-01-15T10:30:00"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 10,
      "total": 1
    }
  }
}
```

### **5. Edit a User**

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "edit",
    "data": {
      "id": 1,
      "full_name": "John Smith",
      "is_admin": true
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Smith",
    "is_active": true,
    "is_admin": true,
    "updated_at": "2024-01-15T11:00:00"
  }
}
```

## 📋 **Task Management Examples**

### **1. Create a New Task**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create",
    "data": {
      "title": "Complete API documentation",
      "description": "Write comprehensive API documentation with examples",
      "status": "pending",
      "priority": "high",
      "due_date": "2024-01-20T17:00:00",
      "owner_id": 1
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Task created successfully",
  "data": {
    "id": 1,
    "title": "Complete API documentation",
    "description": "Write comprehensive API documentation with examples",
    "status": "pending",
    "priority": "high",
    "due_date": "2024-01-20T17:00:00",
    "owner_id": 1,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

### **2. View a Specific Task**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "id": 1
    }
  }'
```

### **3. View Task with Owner Information**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "id": 1,
      "include_owner": true
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Task retrieved successfully",
  "data": {
    "id": 1,
    "title": "Complete API documentation",
    "description": "Write comprehensive API documentation with examples",
    "status": "pending",
    "priority": "high",
    "due_date": "2024-01-20T17:00:00",
    "completed_at": null,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": null,
    "owner": {
      "id": 1,
      "username": "john_doe",
      "full_name": "John Smith",
      "email": "john@example.com"
    }
  }
}
```

### **4. View Tasks by Owner**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "owner_id": 1,
      "page": 1,
      "size": 10
    }
  }'
```

### **5. View Tasks by Status**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "status": "pending",
      "page": 1,
      "size": 10
    }
  }'
```

### **6. Search Tasks**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "search": "documentation",
      "page": 1,
      "size": 10
    }
  }'
```

### **7. Edit a Task**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "edit",
    "data": {
      "id": 1,
      "status": "in_progress",
      "priority": "urgent"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Task updated successfully",
  "data": {
    "id": 1,
    "title": "Complete API documentation",
    "description": "Write comprehensive API documentation with examples",
    "status": "in_progress",
    "priority": "urgent",
    "due_date": "2024-01-20T17:00:00",
    "completed_at": null,
    "updated_at": "2024-01-15T11:30:00"
  }
}
```

### **8. Mark Task as Completed**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "edit",
    "data": {
      "id": 1,
      "status": "completed"
    }
  }'
```

## 🔍 **Advanced View Examples**

### **1. View All Tasks with Pagination**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "page": 1,
      "size": 20
    }
  }'
```

### **2. View Tasks by Priority**

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "priority": "high",
      "page": 1,
      "size": 10
    }
  }'
```

## 🚨 **Error Handling Examples**

### **1. Missing Required Fields**

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create",
    "data": {
      "username": "test_user"
      # Missing email, full_name, password
    }
  }'
```

**Response (Status: 200):**
```json
{
  "success": false,
  "reason": "Missing required field: email"
}
```

### **2. Invalid Action**

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "invalid_action",
    "data": {}
  }'
```

**Response (Status: 200):**
```json
{
  "success": false,
  "reason": "Invalid action: invalid_action"
}
```

### **3. Resource Not Found**

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "data": {
      "id": 999
    }
  }'
```

**Response (Status: 200):**
```json
{
  "success": false,
  "reason": "User not found"
}
```

## 🧪 **Testing with Different Tools**

### **Using Python Requests**

```python
import requests
import json

# Base URL
base_url = "http://localhost:8000/api"

# Create a user
user_data = {
    "action": "create",
    "data": {
        "username": "test_user",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "password123"
    }
}

response = requests.post(f"{base_url}/users", json=user_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
```

### **Using JavaScript/Fetch**

```javascript
// Create a user
const userData = {
  action: "create",
  data: {
    username: "test_user",
    email: "test@example.com",
    full_name: "Test User",
    password: "password123"
  }
};

fetch('http://localhost:8000/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(userData)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### **Using Postman**

1. **Set Method**: POST
2. **Set URL**: `http://localhost:8000/api/users`
3. **Set Headers**: `Content-Type: application/json`
4. **Set Body** (raw JSON):
```json
{
  "action": "create",
  "data": {
    "username": "test_user",
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "password123"
  }
}
```

## 📚 **Next Steps**

After mastering these basic examples:

1. **[Advanced Examples](advanced.md)** - Complex scenarios and workflows
2. **[Testing Guide](testing.md)** - Comprehensive testing strategies
3. **[API Reference](api/overview.md)** - Complete API documentation
4. **[Troubleshooting](../troubleshooting/common.md)** - Common issues and solutions

## 🆘 **Need Help?**

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Examples**: Check the [test script](../../test_api.py) for more examples
- **Issues**: Review the [troubleshooting section](../troubleshooting/common.md)

---

**Happy Coding!** 🚀 These examples should get you started with the API. Experiment with different combinations and explore the interactive documentation!
