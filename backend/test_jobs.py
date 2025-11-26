#!/usr/bin/env python3
"""
Test Jobs endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5001/api/v1"

# Store tokens
employer_token = None
student_token = None
job_id = None

def get_employer_token():
    """Login as employer"""
    print("Logging in as employer...")
    data = {
        "email": "employer1@techcorp.com",
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

def test_create_job(token):
    """Test creating a job posting"""
    print("\nTesting job creation...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Software Engineer Intern",
        "description": "We are looking for a talented software engineering intern to join our team.",
        "job_type": "internship",
        "location": "San Francisco, CA",
        "salary_min": 5000,
        "salary_max": 7000,
        "required_skills": ["Python", "JavaScript", "React"],
        "experience_level": "entry",
        "application_deadline": "2025-12-31"
    }
    response = requests.post(f"{BASE_URL}/jobs", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_get_jobs():
    """Test getting all jobs"""
    print("\nTesting get all jobs...")
    response = requests.get(f"{BASE_URL}/jobs")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Found {len(result.get('data', []))} jobs")
    if result.get('data'):
        print(f"First job: {json.dumps(result['data'][0], indent=2)}")
    return result

def test_apply_to_job(job_id, token):
    """Test applying to a job"""
    print(f"\nTesting job application for job {job_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "cover_letter": "I am very interested in this position and believe I would be a great fit."
    }
    response = requests.post(f"{BASE_URL}/jobs/{job_id}/apply", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

def test_get_job_applications(job_id, token):
    """Test getting applications for a job"""
    print(f"\nTesting get applications for job {job_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/jobs/{job_id}/applications", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()

if __name__ == "__main__":
    print("="*60)
    print("TESTING JOB ENDPOINTS")
    print("="*60)

    # Get tokens
    employer_token = get_employer_token()
    student_token = get_student_token()

    # Test job creation (as employer)
    result = test_create_job(employer_token)
    if 'data' in result and 'job_id' in result['data']:
        job_id = result['data']['job_id']

    # Test get all jobs (public)
    jobs_result = test_get_jobs()
    if not job_id and jobs_result.get('data'):
        job_id = jobs_result['data'][0]['job_id']

    # Test job application (as student)
    if job_id:
        test_apply_to_job(job_id, student_token)

        # Test get applications (as employer)
        test_get_job_applications(job_id, employer_token)

    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)
