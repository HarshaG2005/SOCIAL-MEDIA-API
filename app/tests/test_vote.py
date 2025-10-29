from app.main import limiter
import pytest
from app.main import app


@pytest.fixture(autouse=True)
def reset_rate_limit():
    if hasattr(app.state, "limiter"):
        app.state.limiter.reset()
def test_vote(client_login):
    # First, create a post to vote on
    create_res = client_login.post(
        "/posts/", json={"title": "vote post", "content": "vote content", "published": True}
    )
    assert create_res.status_code == 200
    created_post = create_res.json()
    post_id = created_post['id']
    
    # Cast a vote
    vote_res = client_login.post(
        "/vote/", json={"post_id": post_id, "dir": 1}
    )
    assert vote_res.status_code == 201
    assert vote_res.json() == {"message":"Successfully Voted"}
    
    # Try to cast the same vote again (should fail)
    duplicate_vote_res = client_login.post(
        "/vote/", json={"post_id": post_id, "dir": 1}
    )
    assert duplicate_vote_res.status_code == 409  # Conflict
     
    # Remove the vote
    remove_vote_res = client_login.post(
        "/vote/", json={"post_id": post_id, "dir": 0}
    )
    assert remove_vote_res.status_code == 201
    assert remove_vote_res.json() == {"message":f"Successfully removed vote for post:{post_id}"}
    
    # Try to remove the vote again (should fail)
    duplicate_remove_res = client_login.post(
        "/vote/", json={"post_id": post_id, "dir": 0}
    )
    assert duplicate_remove_res.status_code == 404  # Not Found