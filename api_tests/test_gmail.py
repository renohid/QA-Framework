import os
import requests
import pytest
from pathlib import Path
from dotenv import load_dotenv
from jsonschema import validate

# Build an absolute path to the .env file
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Constants
BASE_URL = "https://gmail.googleapis.com/gmail/v1/users/me/profile"
INVALID_TOKEN = os.environ.get("INVALID_ACCESS_TOKEN")

def get_automated_token():
    """Automatically fetches a fresh 1-hour access token from Google."""
    token_url = "https://oauth2.googleapis.com/token"
    
    payload = {
        "client_id": os.environ.get("GMAIL_CLIENT_ID"),
        "client_secret": os.environ.get("GMAIL_CLIENT_SECRET"),
        "refresh_token": os.environ.get("GMAIL_REFRESH_TOKEN"),
        "grant_type": "refresh_token"
    }
    
    response = requests.post(token_url, data=payload)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to refresh token: {response.text}")

# Dynamically generate a fresh token every time the test suite runs!
VALID_TOKEN = get_automated_token()

# JSON Schema for the Gmail Profile response
PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "emailAddress": {"type": "string", "format": "email"},
        "messagesTotal": {"type": "integer"},
        "threadsTotal": {"type": "integer"},
        "historyId": {"type": "string"}
    },
    "required": ["emailAddress", "messagesTotal", "threadsTotal", "historyId"]
}

def get_headers(token):
    """Helper function to generate authorization headers."""
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

def test_gmail_profile_positive_flow():
    """Validate successful response and correct data values."""
    # Print a safe snippet of the token to verify what is actually being sent
    safe_token = f"{VALID_TOKEN[:10]}...{VALID_TOKEN[-5:]}" if VALID_TOKEN else "None"
    print(f"\nDEBUG - Sending Token: {safe_token}")
    
    response = requests.get(BASE_URL, headers=get_headers(VALID_TOKEN))
    
    if response.status_code != 200:
        print(f"Google API Block Reason: {response.text}")
        
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert "emailAddress" in data
    assert "@gmail.com" in data["emailAddress"]

def test_gmail_profile_negative_flow():
    """Validate error handling by providing an invalid API token."""
    response = requests.get(BASE_URL, headers=get_headers(INVALID_TOKEN))
    
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    
    # Matches Google's exact API error response for invalid credentials
    expected_error = "Request had invalid authentication credentials. Expected OAuth 2 access token, login cookie or other valid authentication credential. See https://developers.google.com/identity/sign-in/web/devconsole-project."
    assert response.json()["error"]["message"] == expected_error

def test_gmail_profile_schema_validation():
    """Use jsonschema to ensure the JSON structure is consistent."""
    response = requests.get(BASE_URL, headers=get_headers(VALID_TOKEN))
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    validate(instance=response.json(), schema=PROFILE_SCHEMA)

def test_gmail_api_performance_check():
    """Log and assert that the API response time is within a professional threshold."""
    response = requests.get(BASE_URL, headers=get_headers(VALID_TOKEN))
    assert response.status_code == 200, "Performance check requires a successful 200 response"
    
    response_time_ms = response.elapsed.total_seconds() * 1000
    print(f"\nAPI Response Time: {response_time_ms:.2f}ms")
    
    # Assert the response time is under 1000ms
    assert response_time_ms < 1000, f"Performance Check Failed: Response took {response_time_ms}ms"