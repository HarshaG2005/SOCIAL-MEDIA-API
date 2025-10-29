# app/tests/test_rate_limiting.py
import time
import pytest
from app.main import app
from app.main import limiter

@pytest.fixture(autouse=True)
def reset_rate_limit():
    if hasattr(app.state, "limiter"):
        app.state.limiter.reset()

def test_login_rate_limit(client_real):
    """Test that login is rate limited after 5 attempts"""
    
    # First 5 attempts should work (or fail with 404/401, but not 429)
    for i in range(5):
        response = client_real.post(
            "/login",
            data={"username": "test@example.com", "password": "passord"}
        )
        assert response.status_code in [401, 404]  # Wrong creds, but not rate limited
    
    # 6th attempt should be rate limited
    response = client_real.post(
        "/login",
        data={"username": 'test@example.com', "password": 'passord'}
    )
    assert response.status_code == 429  # Rate limit exceeded

def test_create_post_rate_limit(client_login):
    """Test that post creation is rate limited"""
    
    # Create 10 posts (should work)
    for i in range(10):
        response = client_login.post(
            "/posts/",
            json={"title": f"Post {i}", "content": f"Content {i}"}
        )
        assert response.status_code == 200
    
    # 11th post should be rate limited
    response = client_login.post(
        "/posts/",
        json={"title": "Post 11", "content": "Content 11"}
    )
    assert response.status_code == 429