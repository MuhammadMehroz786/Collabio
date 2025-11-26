#!/usr/bin/env python3
"""
Test Mentorship endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5001/api/v1"

# Store tokens
mentor_token = None
student_token = None
mentorship_request_id = None

def get_mentor_token():
    """Login as mentor"""
    print("Logging in as mentor...")
    data = {
        "email": "mentor1@company.com",
        "password": "Test1234!"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    result = response.json()
    return result['data']['access_token']

def get_student_token():
    """Login as student"""
    print("Logging in as student...")
    data = {
        "email": "student1@collabio.com",
        "password": "Test1234!"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    result = response.json()
    return result['data']['access_token']

def test_get_mentors():
    """Test getting all mentors (public)"""
    print("\nTesting get all mentors...")
    response = requests.get(f"{BASE_URL}/mentors")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Found {len(result.get('data', {}).get('data', []))} mentors")
    if result.get('data', {}).get('data'):
        print(f"First mentor: {json.dumps(result['data']['data'][0], indent=2)}")
    return result

def test_add_mentor_expertise(token):
    """Test adding expertise to mentor profile"""
    print("\nTesting add mentor expertise...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "expertise_areas": ["Python", "JavaScript", "Software Architecture", "Career Development"]
    }
    response = requests.put(f"{BASE_URL}/mentors/me", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_request_mentorship(mentor_id, token):
    """Test requesting mentorship"""
    print(f"\nTesting mentorship request for mentor {mentor_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "message": "Hi, I'm interested in learning software architecture from you. I'm a computer science student and would love your guidance."
    }
    response = requests.post(f"{BASE_URL}/mentors/{mentor_id}/request", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_get_mentor_requests(token):
    """Test getting mentorship requests (mentor view)"""
    print("\nTesting get mentorship requests (mentor)...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/mentors/requests/received", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_accept_mentorship_request(request_id, token):
    """Test accepting a mentorship request"""
    print(f"\nTesting accept mentorship request {request_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "status": "accepted"
    }
    response = requests.put(f"{BASE_URL}/mentors/requests/{request_id}/status", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

if __name__ == "__main__":
    print("="*60)
    print("TESTING MENTORSHIP ENDPOINTS")
    print("="*60)

    # Get tokens
    mentor_token = get_mentor_token()
    student_token = get_student_token()

    # Update mentor profile with expertise
    test_add_mentor_expertise(mentor_token)

    # Test get all mentors (public)
    mentors_result = test_get_mentors()

    # Get mentor ID
    mentor_id = None
    if mentors_result.get('data', {}).get('data'):
        mentor_id = mentors_result['data']['data'][0]['mentor_id']

    # Test mentorship request (as student)
    if mentor_id:
        request_result = test_request_mentorship(mentor_id, student_token)
        if 'data' in request_result:
            mentorship_request_id = request_result['data'].get('request_id')

    # Test get mentorship requests (as mentor)
    requests_result = test_get_mentor_requests(mentor_token)
    if not mentorship_request_id and requests_result.get('data', {}).get('data'):
        mentorship_request_id = requests_result['data']['data'][0]['request_id']

    # Test accept mentorship request (as mentor)
    if mentorship_request_id:
        test_accept_mentorship_request(mentorship_request_id, mentor_token)

    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)
