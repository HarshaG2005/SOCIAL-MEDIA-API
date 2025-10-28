
def test_create_user(client_real):
    res= client_real.post(
        "/users/",json={"email":"example@gmail.com","password":"password"}
    )
    assert res.status_code==201
    new_user=res.json()
    assert new_user['email']=="example@gmail.com"
    assert 'id' in new_user
    assert 'created_at' in new_user
def test_select_user(client_login):
    res= client_login.get('/users/1')
    assert res.status_code==200
    user=res.json()
    assert user['id']==1
    assert user['email']=="testuser@example.com"
    assert 'created_at' in user
def test_select_nonexistent_user(client_login):
    response = client_login.get('/users/9999')  # Assuming this ID does not exist
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Cant find user related to id:9999'
