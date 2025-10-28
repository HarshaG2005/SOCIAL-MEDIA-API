
def test_create_user_and_select(client_login,client_real):


    # First, create a user to ensure there is one to retrieve
    create_response = client_real.post('/users/', json={
        "email": f'test1@gmail.com',
        "password": 'test123'
    })
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert 'id' in created_user
    user_id = created_user['id']
    # Now, retrieve the user by ID
    select_response = client_login.get(f'/users/{user_id}')
    assert select_response.status_code == 200
    selected_user = select_response.json()
    assert selected_user['email'] == 'test1@gmail.com'
    assert selected_user['id'] == user_id
def test_select_nonexistent_user(client_login):
    response = client_login.get('/users/9999')  # Assuming this ID does not exist
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Cant find user related to id:9999'