# 🔌 API Overview

Comprehensive guide to the User Account and Tasks API architecture, design principles, and core concepts.

## 🏗️ **Architecture Overview**

The API follows a **layered architecture** pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│                        API Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ User Routes │  │ Task Routes │  │   Global Handlers   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                     Service Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │User Service │  │Task Service │  │   Auth Service      │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                     Data Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Models    │  │  Schemas    │  │   Database          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 **Design Principles**

### **1. Simplified Response System**
- **Only two HTTP status codes**: 200 (success/error) and 500 (server error)
- **Client errors return 200** with error details in `reason` field
- **Server errors return 500** for genuine system failures

### **2. Action-Based Architecture**
- **All endpoints are POST** for consistency
- **Three core actions**: `create`, `edit`, `view`
- **Unified request format** across all endpoints

### **3. RESTful Design**
- **Resource-based URLs**: `/api/users`, `/api/tasks`
- **CRUD operations** through action parameter
- **Consistent response format** for all operations

## 📡 **Request/Response Format**

### **Request Structure**
```json
{
  "action": "create|edit|view",
  "data": {
    // Action-specific data
  }
}
```

### **Response Structure**
```json
{
  "success": true|false,
  "message": "Success/error message",
  "data": {
    // Response data (for success)
  },
  "reason": "Error reason (for failures)"
}
```

## 🔄 **HTTP Status Code Strategy**

| Scenario | Status Code | Response Format |
|----------|-------------|-----------------|
| **Successful operation** | 200 | `{"success": true, "data": {...}}` |
| **Client error** | 200 | `{"success": false, "reason": "..."}` |
| **Server error** | 500 | `{"success": false, "reason": "..."}` |

### **Why This Approach?**

1. **Simplified client logic** - Only handle 200/500
2. **Better error handling** - Errors always include descriptive reasons
3. **Consistent interface** - Same response structure for all scenarios
4. **Monitoring friendly** - Easy to distinguish client vs server issues

## 🛣️ **API Endpoints**

### **Base URL**
```
http://localhost:8000/api
```

### **Available Endpoints**

| Endpoint | Purpose | Actions Supported |
|----------|---------|-------------------|
| `/api/users` | User management | create, edit, view |
| `/api/tasks` | Task management | create, edit, view |

### **Endpoint Patterns**
```
POST /api/users
POST /api/tasks
```

## 🔐 **Authentication & Security**

### **Current Implementation**
- **Password hashing** with bcrypt
- **Input validation** with Pydantic schemas
- **SQL injection protection** via SQLAlchemy ORM
- **CORS configuration** for cross-origin requests

### **Security Features**
- **Non-root Docker user** for container security
- **Environment variable** configuration
- **Input sanitization** and validation
- **Error message sanitization** (no internal details exposed)

## 📊 **Data Models**

### **User Model**
```python
class User(Base):
    id: int (Primary Key)
    username: str (Unique)
    email: str (Unique)
    full_name: str
    hashed_password: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
```

### **Task Model**
```python
class Task(Base):
    id: int (Primary Key)
    title: str
    description: str (Optional)
    status: TaskStatus (Enum)
    priority: TaskPriority (Enum)
    due_date: datetime (Optional)
    completed_at: datetime (Optional)
    owner_id: int (Foreign Key to User)
    created_at: datetime
    updated_at: datetime
```

### **Enums**
```python
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
```

## 🔄 **Action Types**

### **Create Action**
- **Purpose**: Create new resources
- **Required fields**: Varies by resource type
- **Response**: New resource data with ID

### **Edit Action**
- **Purpose**: Update existing resources
- **Required fields**: Resource ID + fields to update
- **Response**: Updated resource data

### **View Action**
- **Purpose**: Retrieve resource(s)
- **Required fields**: Varies (ID, filters, pagination)
- **Response**: Resource data or list of resources

## 📝 **Validation & Error Handling**

### **Input Validation**
- **Pydantic schemas** for request validation
- **Field constraints** (min/max length, required fields)
- **Type validation** (email, datetime, enums)
- **Custom validators** for business logic

### **Error Handling Strategy**
```python
try:
    # Business logic
    result = service.perform_action(data)
    return APIResponse.success(result)
except ValueError as e:
    # Client error - return 200 with reason
    return APIResponse.error(str(e))
except Exception as e:
    # Server error - return 500
    return APIResponse.server_error("Internal server error")
```

## 🗄️ **Database Design**

### **SQLite Database**
- **File-based** for simplicity and portability
- **Automatic schema creation** on startup
- **ACID compliance** for data integrity
- **Relationship support** between users and tasks

### **Key Relationships**
- **User → Tasks**: One-to-many relationship
- **Cascade deletion**: Deleting user removes their tasks
- **Foreign key constraints** for data integrity

## 📈 **Performance Considerations**

### **Optimization Features**
- **Database indexing** on frequently queried fields
- **Pagination support** for large result sets
- **Efficient queries** with SQLAlchemy ORM
- **Connection pooling** for database connections

### **Scalability Features**
- **Stateless design** for horizontal scaling
- **Docker containerization** for easy deployment
- **Resource limits** to prevent resource exhaustion
- **Health checks** for load balancer integration

## 🔍 **Monitoring & Observability**

### **Logging Strategy**
- **Structured logging** with consistent format
- **Log levels** (DEBUG, INFO, WARNING, ERROR)
- **Log rotation** to prevent disk space issues
- **Context information** (function names, line numbers)

### **Health Monitoring**
- **Health endpoint** (`/health`) for monitoring
- **Docker health checks** for container monitoring
- **Response time tracking** in logs
- **Error rate monitoring** via log analysis

## 🚀 **Deployment Architecture**

### **Container Strategy**
- **Single container** deployment for simplicity
- **Multi-stage builds** for production optimization
- **Environment-specific** configurations
- **Volume mounting** for persistent data

### **Configuration Management**
- **Environment variables** for configuration
- **Docker Compose** for orchestration
- **Health checks** for automated monitoring
- **Resource limits** for production stability

## 🔮 **Future Enhancements**

### **Planned Features**
- **JWT authentication** for secure API access
- **Rate limiting** to prevent abuse
- **API versioning** for backward compatibility
- **GraphQL support** for flexible queries
- **Real-time updates** with WebSocket support

### **Scalability Improvements**
- **PostgreSQL support** for larger datasets
- **Redis caching** for performance
- **Message queues** for async processing
- **Microservices architecture** for complex deployments

## 📚 **API Documentation**

### **Interactive Documentation**
- **Swagger UI**: `/docs` - Interactive API explorer
- **ReDoc**: `/redoc` - Clean, responsive documentation
- **OpenAPI specification** for code generation
- **Example requests** for all endpoints

### **Documentation Features**
- **Request/response examples** for all actions
- **Schema definitions** for all data types
- **Error code explanations** and solutions
- **Authentication examples** and setup

## 🧪 **Testing Strategy**

### **Testing Approach**
- **Integration tests** with test database
- **API endpoint testing** with real HTTP requests
- **Error scenario testing** for robust error handling
- **Performance testing** for scalability validation

### **Test Coverage**
- **All endpoints** tested for success and failure
- **All action types** validated with various inputs
- **Error conditions** tested for proper handling
- **Edge cases** covered for robustness

---

**Next Steps**: Explore the [User Endpoints](users.md) and [Task Endpoints](tasks.md) to understand specific API usage patterns.
