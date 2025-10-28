import pytest
from app.main import app
from fastapi.testclient import TestClient
from app.oauth2 import get_current_user
class FakeUser:
    def __init__(self, id:int=1):
        self.id = id
        # self.email = email

 
def override_get_current_user():
    return FakeUser(1)

@pytest.fixture
def client_login():
    app.dependency_overrides[get_current_user]=override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def client_real():
    return TestClient(app)
