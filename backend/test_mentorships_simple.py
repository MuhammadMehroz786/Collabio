#!/usr/bin/env python3
"""
Test Mentorship endpoints (simplified)
"""
import requests
import json

BASE_URL = "http://localhost:5001/api/v1"

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
    data_list = result.get('data', {}).get('data', [])
    print(f"Found {len(data_list)} mentors")
    if data_list:
        print(f"First mentor: {json.dumps(data_list[0], indent=2)}")
    return result

def test_request_mentorship(mentor_id, token):
    """Test requesting mentorship"""
    print(f"\nTesting mentorship request for mentor {mentor_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "message": "Hi, I'm interested in learning software architecture from you."
    }
    response = requests.post(f"{BASE_URL}/mentors/{mentor_id}/request", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_get_mentor_requests(token):
    """Test getting mentorship requests (mentor view)"""
    print("\nTesting get mentorship requests (mentor)...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/mentors/requests/my", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_respond_to_request(request_id, token):
    """Test accepting a mentorship request"""
    print(f"\nTesting accept mentorship request {request_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "status": "accepted"
    }
    response = requests.put(f"{BASE_URL}/mentors/requests/{request_id}/respond", json=data, headers=headers)
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

    # Test get all mentors (public)
    mentors_result = test_get_mentors()

    # Get mentor ID
    mentor_id = None
    if mentors_result.get('data', {}).get('data'):
        mentor_id = mentors_result['data']['data'][0]['mentor_id']

    # Test mentorship request (as student)
    mentorship_request_id = None
    if mentor_id:
        request_result = test_request_mentorship(mentor_id, student_token)
        if 'data' in request_result:
            mentorship_request_id = request_result['data'].get('request_id')

    # Test get mentorship requests (as mentor)
    requests_result = test_get_mentor_requests(mentor_token)
    if not mentorship_request_id and requests_result.get('data', {}).get('data'):
        mentorship_request_id = requests_result['data']['data'][0]['request_id']

    # Test respond to mentorship request (as mentor)
    if mentorship_request_id:
        test_respond_to_request(mentorship_request_id, mentor_token)

    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)
