# import pytest
# from fastapi.testclient import TestClient
# from ..main import app
# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import os, sys
# from fastapi.testclient import TestClient

# # ✅ Add the project root to Python path (1 level above 'app')
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from app.main import app  # ✅ import the FastAPI app

# client = TestClient(app)


# from main import app
#   # change path if needed

# client = TestClient(app)

# def test_home_unauthorized():
#     res = client.get("/posts/")
#     assert res.status_code == 401
import os, sys
from fastapi.testclient import TestClient

# ✅ Add the project root to Python path (1 level above 'app')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app  # import your FastAPI app

client = TestClient(app)

def test_home_unauthorized():
    res = client.get("/posts/")
    assert res.status_code == 401
