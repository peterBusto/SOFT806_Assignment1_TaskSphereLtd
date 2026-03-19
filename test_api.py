#!/usr/bin/env python
"""
Simple test script to verify API endpoints are working.
Run this script to test the API endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api_endpoints():
    print("Testing TaskSphere API Endpoints")
    print("=" * 40)
    
    # Test endpoints that don't require authentication
    endpoints = [
        ("/projects", "Projects List"),
        ("/tasks", "Tasks List"),
        ("/users", "Users List"),
    ]
    
    for endpoint, name in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            print(f"\nTesting {name}: {url}")
            
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 401:
                print("✓ Endpoint exists but requires authentication (expected)")
            elif response.status_code == 200:
                print("✓ Endpoint accessible")
                data = response.json()
                if isinstance(data, dict) and 'results' in data:
                    print(f"  Results count: {len(data['results'])}")
                elif isinstance(data, list):
                    print(f"  Results count: {len(data)}")
            else:
                print(f"✗ Unexpected response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("✗ Connection failed - make sure the server is running")
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
    print("\n" + "=" * 40)
    print("API Test Complete!")
    print("\nAvailable API Endpoints:")
    print("- GET /api/projects/ - List projects (auth required)")
    print("- POST /api/projects/ - Create project (auth required)")
    print("- GET /api/projects/{id}/ - Get project details (auth required)")
    print("- PUT /api/projects/{id}/ - Update project (auth required)")
    print("- DELETE /api/projects/{id}/ - Delete project (auth required)")
    print("- GET /api/projects/{id}/tasks/ - Get project tasks (auth required)")
    print()
    print("- GET /api/tasks/ - List tasks (auth required)")
    print("- POST /api/tasks/ - Create task (auth required)")
    print("- GET /api/tasks/{id}/ - Get task details (auth required)")
    print("- PUT /api/tasks/{id}/ - Update task (auth required)")
    print("- DELETE /api/tasks/{id}/ - Delete task (auth required)")
    print("- GET /api/tasks/my_tasks/ - Get my assigned tasks (auth required)")
    print("- GET /api/tasks/by_status/?status=todo - Get tasks by status (auth required)")
    print()
    print("- GET /api/users/ - List users (auth required)")
    print("- GET /api/users/{id}/ - Get user details (auth required)")
