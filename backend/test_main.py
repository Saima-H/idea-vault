from fastapi.testclient import TestClient
from main import app
import pytest
from jose import jwt

client = TestClient(app)

# Fake Tokens for testing
SAIMA_TOKEN = "Bearer fake-token-for-saima"
ALEX_TOKEN = "Bearer fake-token-for-alex"

# Mock the token decoding so it doesn't fail on fake tokens
def mock_get_unverified_claims(token):
    if "saima" in token:
        return {"email": "saima@test.com"}
    elif "alex" in token:
        return {"email": "alex@test.com"}
    return {}

jwt.get_unverified_claims = mock_get_unverified_claims

# TEST 1: No token provided
def test_get_ideas_requires_auth():
    response = client.get("/ideas")
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing Authorization Header"
# TEST 2: Create an idea successfully
def test_create_idea():
    response = client.post(
        "/ideas",
        json={"user_id": "saima@test.com", "content": "Pytest idea", "url": None},
        headers={"Authorization": SAIMA_TOKEN}
    )
    assert response.status_code == 200
    assert response.json()["content"] == "Pytest idea"

# TEST 3: CRITICAL - User A cannot see User B's ideas
def test_get_ideas_isolation():
    # Saima creates a secret idea
    client.post(
        "/ideas",
        json={"user_id": "saima@test.com", "content": "Saima's secret", "url": None},
        headers={"Authorization": SAIMA_TOKEN}
    )
    
    # Alex asks for his ideas
    response = client.get("/ideas", headers={"Authorization": ALEX_TOKEN})
    data = response.json()
    
    # Assert Alex cannot see Saima's secret
    for idea in data:
        assert idea["content"] != "Saima's secret"

# TEST 4: Cannot create an idea for someone else
def test_create_idea_for_other_user_fails():
    response = client.post(
        "/ideas",
        json={"user_id": "alex@test.com", "content": "Hacked idea", "url": None},
        headers={"Authorization": SAIMA_TOKEN} # Using Saima's token
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "You can only create ideas for yourself"

# TEST 5: Invalid token
def test_invalid_token():
    response = client.get("/ideas", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401