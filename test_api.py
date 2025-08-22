#!/usr/bin/env python3
"""
Test script for the User Account and Tasks API
This script demonstrates how to use the API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    """Test the API endpoints."""
    print("🚀 Testing User Account and Tasks API")
    print("=" * 50)
    
    # Test 1: Create a user
    print("\n1. Creating a user...")
    user_data = {
        "action": "create",
        "data": {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "securepassword123",
            "is_active": True,
            "is_admin": False
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/users", json=user_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200 and response.json().get("success"):
        user_id = response.json()["data"]["id"]
        print(f"✅ User created with ID: {user_id}")
    else:
        print("❌ Failed to create user")
        return
    
    # Test 2: Create another user
    print("\n2. Creating another user...")
    user_data2 = {
        "action": "create",
        "data": {
            "username": "jane_smith",
            "email": "jane@example.com",
            "full_name": "Jane Smith",
            "password": "securepassword456",
            "is_active": True,
            "is_admin": False
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/users", json=user_data2)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200 and response.json().get("success"):
        user2_id = response.json()["data"]["id"]
        print(f"✅ User created with ID: {user2_id}")
    else:
        print("❌ Failed to create second user")
        user2_id = None
    
    # Test 3: View all users
    print("\n3. Viewing all users...")
    view_users_data = {
        "action": "view",
        "data": {
            "page": 1,
            "size": 10
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/users", json=view_users_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 4: Create a task for the first user
    print("\n4. Creating a task...")
    task_data = {
        "action": "create",
        "data": {
            "title": "Complete API documentation",
            "description": "Write comprehensive API documentation with examples",
            "status": "pending",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "owner_id": user_id
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200 and response.json().get("success"):
        task_id = response.json()["data"]["id"]
        print(f"✅ Task created with ID: {task_id}")
    else:
        print("❌ Failed to create task")
        return
    
    # Test 5: Create another task
    print("\n5. Creating another task...")
    task_data2 = {
        "action": "create",
        "data": {
            "title": "Review code",
            "description": "Review pull requests and provide feedback",
            "status": "in_progress",
            "priority": "medium",
            "owner_id": user_id
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data2)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 6: View tasks by owner
    print("\n6. Viewing tasks by owner...")
    view_tasks_data = {
        "action": "view",
        "data": {
            "owner_id": user_id,
            "page": 1,
            "size": 10
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks", json=view_tasks_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 7: Edit a task
    print("\n7. Editing a task...")
    edit_task_data = {
        "action": "edit",
        "data": {
            "id": task_id,
            "status": "in_progress",
            "priority": "urgent"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks", json=edit_task_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 8: View specific task
    print("\n8. Viewing specific task...")
    view_task_data = {
        "action": "view",
        "data": {
            "id": task_id,
            "include_owner": True
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks", json=view_task_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 9: Search tasks
    print("\n9. Searching tasks...")
    search_tasks_data = {
        "action": "view",
        "data": {
            "search": "documentation",
            "page": 1,
            "size": 10
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks", json=search_tasks_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 10: Test error handling (invalid action)
    print("\n10. Testing error handling (invalid action)...")
    invalid_data = {
        "action": "invalid_action",
        "data": {}
    }
    
    response = requests.post(f"{BASE_URL}/api/users", json=invalid_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 11: Test error handling (missing required fields)
    print("\n11. Testing error handling (missing required fields)...")
    incomplete_data = {
        "action": "create",
        "data": {
            "username": "test_user"
            # Missing email, full_name, password
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/users", json=incomplete_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("\nNote: All responses should return status code 200 (even for errors)")
    print("Errors are returned with success: false and reason field")
    print("Only server errors return status code 500")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API. Make sure it's running on http://localhost:8000")
        print("Start the API with: python start.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
