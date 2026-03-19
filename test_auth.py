#!/usr/bin/env python
"""
Test script for authentication endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_authentication():
    print("Testing Authentication Endpoints")
    print("=" * 40)
    
    # Test registration
    print("\n1. Testing User Registration")
    registration_data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "profile": {
            "bio": "Test user bio",
            "company": "Test Company",
            "position": "Developer"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=registration_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print("✓ Registration successful")
            print(f"Response: {response.json()}")
        else:
            print(f"✗ Registration failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test login
    print("\n2. Testing User Login")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Login successful")
            print(f"Response: {response.json()}")
        else:
            print(f"✗ Login failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test current user endpoint (will fail without authentication)
    print("\n3. Testing Current User Endpoint (without auth)")
    try:
        response = requests.get(f"{BASE_URL}/auth/me/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 401:
            print("✓ Correctly requires authentication")
        else:
            print(f"✗ Unexpected response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_authentication()
    print("\n" + "=" * 40)
    print("Authentication Test Complete!")
    print("\nAvailable Authentication Endpoints:")
    print("- POST /api/auth/register/ - Register new user")
    print("- POST /api/auth/login/ - Login user")
    print("- POST /api/auth/logout/ - Logout user (auth required)")
    print("- GET /api/auth/me/ - Get current user (auth required)")
    print("- GET /api/auth/profile/ - Get user profile (auth required)")
    print("- PUT /api/auth/profile/ - Update user profile (auth required)")
