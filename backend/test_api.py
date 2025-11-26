#!/usr/bin/env python3
"""
Test API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5001/api/v1"

def test_register_student():
    """Test student registration"""
    print("Testing student registration...")
    data = {
        "email": "student1@collabio.com",
        "password": "Test1234!",
        "user_type": "student",
        "full_name": "John Doe"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_login(email, password):
    """Test login"""
    print(f"\nTesting login for {email}...")
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_register_employer():
    """Test employer registration"""
    print("\nTesting employer registration...")
    data = {
        "email": "employer1@techcorp.com",
        "password": "Test1234!",
        "user_type": "employer",
        "company_name": "TechCorp Inc"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_register_mentor():
    """Test mentor registration"""
    print("\nTesting mentor registration...")
    data = {
        "email": "mentor1@company.com",
        "password": "Test1234!",
        "user_type": "mentor",
        "full_name": "Jane Smith",
        "current_role": "Senior Software Engineer",
        "current_company": "Big Tech Co"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

if __name__ == "__main__":
    print("="*60)
    print("TESTING AUTHENTICATION ENDPOINTS")
    print("="*60)

    # Test student registration
    result = test_register_student()

    # Test student login
    if 'data' in result and 'user' in result.get('data', {}):
        test_login("student1@collabio.com", "Test1234!")

    # Test employer registration
    test_register_employer()

    # Test mentor registration
    test_register_mentor()

    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)
