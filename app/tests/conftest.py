import os
os.environ["TESTING"] = "1"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.databases import get_db, Base
from app.oauth2 import get_current_user
import app.models 
from app.main import app as app1
# Test database (SQLite for fast isolated tests)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
# with engine.connect() as conn:
#     conn.execute("PRAGMA foreign_keys=ON;")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class FakeUser:
    def __init__(self, id: int = 1):
        self.id = id

def override_get_current_user():
    return FakeUser(1)

def override_get_db():
    
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def setup_database():
    """Create fresh tables for each test"""
    
    Base.metadata.create_all(bind=engine)
    
    #  CREATE A TEST USER IN THE DATABASE
    db = TestingSessionLocal()
    try:
        test_user = app.models.User(
            id=1,
            email="testuser@example.com",
            password=app.utils.hash("password")
        )
        db.add(test_user)
        db.commit()
    finally:
        db.close()
    
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client_login(setup_database):
    """Test client with authentication"""
    # app.dependency_overrides[get_current_user] = override_get_current_user
    app1.dependency_overrides[get_db] = override_get_db
    app1.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app1)
    app1.dependency_overrides.clear()

@pytest.fixture
def client_real(setup_database):
    """Test client without authentication"""
    app1.dependency_overrides[get_db] = override_get_db
    yield TestClient(app1)
    app1.dependency_overrides.clear()