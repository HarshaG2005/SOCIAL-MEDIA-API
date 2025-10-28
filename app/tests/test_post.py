# Add the project root to Python path (1 level above 'app')
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def test_create_post(client_login):
    res= client_login.post(
        "/posts/",json={"title":"test post","content":"test content","published":True}

    )
    print(res.text)

    assert res.status_code==200

    new_post=res.json()
    assert new_post['title']=="test post"
    assert new_post['content']=="test content"
    assert new_post['published']==True
    assert 'id' in new_post
    assert 'owner_id' in new_post
    assert 'created_at' in new_post



def test_get_all_post(client_login):
    res=client_login.get(
        "/posts/"
    )
    assert res.status_code==200
    posts=res.json()
    assert isinstance(posts,list)
    for post in posts:
        assert  'post' in post
        assert 'votes' in post
        assert 'id' in post['post']
        assert 'title' in post['post']
        assert 'content' in post['post']
        assert 'published' in post['post']
        assert 'owner_id' in post['post']
        assert 'created_at' in post['post']

def test_select_post_by_id(client_login):
    # First, create a post to ensure there is one to retrieve
    create_res = client_login.post(
        "/posts/", json={"title": "specific post", "content": "specific content", "published": True}
    )
    assert create_res.status_code == 200
    created_post = create_res.json()
    post_id = created_post['id']
    # Now, retrieve the post by its ID
    res = client_login.get(f"/posts/{post_id}")
    assert res.status_code == 200
    post = res.json()
    assert post['post']['id'] == post_id
    assert post['post']['title'] == "specific post"
    assert post['post']['content'] == "specific content"
    assert post['post']['published'] == True
    assert post['post']['owner_id'] == created_post['owner_id']
    assert 'created_at' in post['post']

def test_update_post(client_login):
    # First, create a post to ensure there is one to update
    create_res = client_login.post(
        "/posts/", json={"title": "old title", "content": "old content", "published": True}
    )
    assert create_res.status_code == 200
    created_post = create_res.json()
    post_id= created_post['id']
    # Now, update the post
    updated_res = client_login.put(
        f"/posts/{post_id}",
        json={"title":"new title","content":"new content","published":True}
    )
    assert updated_res.status_code == 200
    updated_post = updated_res.json()
    assert updated_post['new']['title'] == "new title"
    assert updated_post['new']['content'] == "new content"
    assert updated_post['new']['published'] == True
    assert updated_post['new']['id'] == post_id
    assert updated_post['new']['owner_id'] == created_post['owner_id']
    assert 'created_at' in updated_post['new']
def test_delete_post(client_login):
    # First, create a post to ensure there is one to delete
    create_res = client_login.post(
        "/posts/", json={"title": "to be deleted", "content": "to be deleted content", "published": True}
    )
    assert create_res.status_code == 200
    created_post = create_res.json()
    post_id= created_post['id']
    # Now, delete the post
    delete_res = client_login.delete(f"/posts/{post_id}")
    assert delete_res.status_code == 200
    delete_msg = delete_res.json()
    assert delete_msg['message'] == "post deleted successfully"
    # Verify the post has been deleted
    get_res = client_login.get(f"/posts/{post_id}")
    assert get_res.status_code == 404