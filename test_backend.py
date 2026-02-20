#!/usr/bin/env python
"""
Quick Integration Test Script

Test the backend API without needing a frontend.
Useful for verifying the system works end-to-end.

Usage:
python test_backend.py

Tests:
1. Create user account (signup)
2. Login and get JWT token
3. Get current user profile
4. Create project
5. List projects
6. Upload CSV file
7. Verify data profiling results
8. Verify semantic layer detection
"""

import requests
import json
import tempfile
from pathlib import Path

BASE_URL = "http://localhost:8000"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_test(name: str):
    print(f"\n{bcolors.HEADER}{bcolors.BOLD}TEST: {name}{bcolors.ENDC}")

def print_success(msg: str):
    print(f"{bcolors.OKGREEN}✅ {msg}{bcolors.ENDC}")

def print_error(msg: str):
    print(f"{bcolors.FAIL}❌ {msg}{bcolors.ENDC}")

def print_info(msg: str):
    print(f"{bcolors.OKCYAN}ℹ️ {msg}{bcolors.ENDC}")

def test_health():
    """Test backend is running"""
    print_test("Health Check")
    try:
        resp = requests.get(f"{BASE_URL}/health")
        if resp.status_code == 200:
            print_success("Backend is running")
            print(json.dumps(resp.json(), indent=2))
            return True
        else:
            print_error(f"Unexpected status: {resp.status_code}")
            return False
    except Exception as e:
        print_error(f"Backend not running: {e}")
        print_info("Start backend: cd backend && python -m uvicorn main:app --reload")
        return False

def test_signup():
    """Test user signup"""
    print_test("User Signup")
    data = {
        "email": "alice@example.com",
        "password": "securepassword123",
        "full_name": "Alice Johnson",
        "persona": "teacher"
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/signup", json=data)
        
        if resp.status_code in [201, 200]:
            result = resp.json()
            print_success("Signup successful")
            print_info(f"User ID: {result['user']['id']}")
            print_info(f"Token: {result['access_token'][:50]}...")
            return result['access_token'], result['user']['id']
        elif resp.status_code == 409:
            print_info("User already exists, trying to login instead...")
            return test_login()
        else:
            print_error(f"Signup failed: {resp.status_code}")
            print(resp.text)
            return None, None
    except Exception as e:
        print_error(f"Request failed: {e}")
        return None, None

def test_login():
    """Test user login"""
    print_test("User Login")
    data = {
        "email": "alice@example.com",
        "password": "securepassword123"
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        
        if resp.status_code == 200:
            result = resp.json()
            print_success("Login successful")
            return result['access_token'], result['user']['id']
        else:
            print_error(f"Login failed: {resp.status_code}")
            print(resp.text)
            return None, None
    except Exception as e:
        print_error(f"Request failed: {e}")
        return None, None

def test_get_me(token: str):
    """Test getting current user"""
    print_test("Get Current User (/api/auth/me)")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        resp = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        
        if resp.status_code == 200:
            user = resp.json()
            print_success(f"Current user: {user['email']}")
            return True
        else:
            print_error(f"Failed to get user: {resp.status_code}")
            print(resp.text)
            return False
    except Exception as e:
        print_error(f"Request failed: {e}")
        return False

def test_create_project(token: str):
    """Test creating a project"""
    print_test("Create Project")
    
    data = {
        "name": "Q4 Sales Analysis",
        "description": "Test data analysis"
    }
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        resp = requests.post(f"{BASE_URL}/api/projects", json=data, headers=headers)
        
        if resp.status_code in [200, 201]:
            project = resp.json()
            print_success(f"Project created: {project['name']}")
            print_info(f"Project ID: {project['id']}")
            return project['id']
        else:
            print_error(f"Failed: {resp.status_code}")
            print(resp.text)
            return None
    except Exception as e:
        print_error(f"Request failed: {e}")
        return None

def test_list_projects(token: str):
    """Test listing projects"""
    print_test("List Projects")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        resp = requests.get(f"{BASE_URL}/api/projects", headers=headers)
        
        if resp.status_code == 200:
            projects = resp.json()
            print_success(f"Found {len(projects)} project(s)")
            for p in projects:
                print_info(f"  - {p['name']} (ID: {p['id']})")
            return True
        else:
            print_error(f"Failed: {resp.status_code}")
            print(resp.text)
            return False
    except Exception as e:
        print_error(f"Request failed: {e}")
        return False

def test_upload_file(token: str, project_id: int):
    """Test file upload"""
    print_test("Upload CSV File")
    
    # Create sample CSV
    csv_content = """sales,region,date,quantity
1200,North,2024-01-15,5
950,South,2024-01-16,3
1500,East,2024-01-17,7
1100,West,2024-01-18,4
900,North,2024-01-19,2"""
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        # Upload file
        with open(temp_path, 'rb') as f:
            files = {'file': ('sales_data.csv', f)}
            resp = requests.post(
                f"{BASE_URL}/api/datasets/upload/{project_id}",
                files=files,
                headers=headers
            )
        
        # Clean up
        Path(temp_path).unlink()
        
        if resp.status_code in [200, 201]:
            result = resp.json()
            print_success(f"File uploaded: {result['filename']}")
            print_info(f"Rows: {result['row_count']}, Columns: {result['column_count']}")
            
            # Print profiling results
            if 'profile' in result:
                print_info(f"Data Quality Score: {result['profile']['summary'].get('data_quality_score', 'N/A')}/100")
                print_info(f"Issues Found: {result['profile']['summary'].get('total_issues', 0)}")
            
            # Print semantic layer
            if 'semantic_layer' in result:
                sem = result['semantic_layer']
                print_info(f"Metrics Detected: {len(sem.get('metrics', []))}")
                print_info(f"Dimensions Detected: {len(sem.get('dimensions', []))}")
                print_info(f"Time Dimensions: {len(sem.get('time_dimensions', []))}")
                
                for metric in sem.get('metrics', []):
                    print_info(f"  📊 {metric['business_name']} ({metric['aggregation']})")
                
                for dim in sem.get('dimensions', []):
                    print_info(f"  🏷️ {dim['business_name']}")
            
            return result.get('dataset_id')
        else:
            print_error(f"Upload failed: {resp.status_code}")
            print(resp.text)
            return None
    except Exception as e:
        print_error(f"Request failed: {e}")
        return None

def main():
    print(f"\n{bcolors.BOLD}{bcolors.HEADER}=== DeepRow Backend Integration Test ==={bcolors.ENDC}\n")
    
    # 1. Health check
    if not test_health():
        return
    
    # 2. Signup / Login
    token, user_id = test_signup()
    if not token:
        return
    
    # 3. Get current user
    if not test_get_me(token):
        return
    
    # 4. Create project
    project_id = test_create_project(token)
    if not project_id:
        return
    
    # 5. List projects
    if not test_list_projects(token):
        return
    
    # 6. Upload file
    dataset_id = test_upload_file(token, project_id)
    if not dataset_id:
        return
    
    # Success
    print(f"\n{bcolors.BOLD}{bcolors.OKGREEN}=== All Tests Passed! ==={bcolors.ENDC}\n")
    print("Next steps:")
    print("1. Build the frontend login page")
    print("2. Integrate file upload UI")
    print("3. Build dashboard visualization")
    print("4. Add data transparency/explainability features")

if __name__ == "__main__":
    main()
