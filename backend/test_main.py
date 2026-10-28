from fastapi.testclient import TestClient
from main import app
import pytest
import os
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

client = TestClient(app)
SECRET_KEY = os.getenv("SUPABASE_JWT_SECRET")

def create_test_token(email: str):
    payload = {
        "email": email,
        "aud": "authenticated",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

SAIMA_TOKEN = f"Bearer {create_test_token('saima@test.com')}"
ALEX_TOKEN = f"Bearer {create_test_token('alex@test.com')}"

def test_get_ideas_requires_auth():
    response = client.get("/ideas")
    assert response.status_code == 401

def test_create_idea():
    response = client.post(
        "/ideas",
        json={"content": "Pytest secure idea", "url": None},
        headers={"Authorization": SAIMA_TOKEN}
    )
    assert response.status_code == 200

def test_get_ideas_isolation():
    client.post(
        "/ideas",
        json={"content": "Saima's secure secret", "url": None},
        headers={"Authorization": SAIMA_TOKEN}
    )
    response = client.get("/ideas", headers={"Authorization": ALEX_TOKEN})
    data = response.json()
    for idea in data:
        assert idea["content"] != "Saima's secure secret"

def test_invalid_token():
    response = client.get("/ideas", headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401