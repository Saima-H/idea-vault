from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_hack_read_alex_ideas():
    """
    EXPLOIT: Forging a token with NO valid signature.
    If this passes, the backend is accepting fake identities.
    """
    # A fake token claiming to be alex@test.com
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFsZXhAdGVzdC5jb20ifQ.fake_signature_hacker"
    
    response = client.get(
        "/ideas",
        headers={"Authorization": f"Bearer {fake_token}"}
    )
    
    print("\nServer Response:", response.json())
    # If we get 200 OK, we successfully hacked the app
    assert response.status_code == 200