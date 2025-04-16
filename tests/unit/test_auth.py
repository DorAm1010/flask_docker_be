from unittest.mock import MagicMock, patch


def test_signup_missing_fields(client):
    response = client.post('/auth/signup', json={})
    assert response.status_code == 400
    assert b'Missing required fields' in response.data

@patch('app.routes.auth_routes.User.query')
@patch('app.routes.auth_routes.db.session')
def test_signup_user_already_exists(mock_session, mock_query, client):
    mock_query.filter.return_value.first.return_value = True
    payload = {"username": "john", "email": "john@example.com", "password": "somPass123!"}
    response = client.post('/auth/signup', json=payload)
    assert response.status_code == 409
    assert b'User with given email already exists' in response.data

@patch('app.routes.auth_routes.db.session')
@patch('app.routes.auth_routes.User.query')
def test_signup_success(mock_query, mock_session, client):
    mock_query.filter.return_value.first.return_value = None
    payload = {"username": "john", "email": "john@example.com", "password": "somPass123!"}
    response = client.post('/auth/signup', json=payload)
    assert response.status_code == 201
    assert b'created successfully' in response.data

@patch('app.routes.auth_routes.User.query')
def test_get_user_success(mock_query, client):
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = 'john'
    mock_query.get_or_404.return_value = mock_user

    response = client.get('/auth/1')
    assert response.status_code == 200
    assert b'john' in response.data

@patch('app.routes.auth_routes.User.query')
def test_login_success(mock_query, client):
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = 'john'
    mock_user.check_password.return_value = True
    mock_query.filter_by.return_value.first_or_404.return_value = mock_user

    response = client.post('/auth/login', json={
        "email": "john@example.com",
        "password": "123"
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data

@patch('app.routes.auth_routes.User.query')
def test_login_failure(mock_query, client):
    mock_user = MagicMock()
    mock_user.check_password.return_value = False
    mock_query.filter_by.return_value.first_or_404.return_value = mock_user

    response = client.post('/auth/login', json={
        "email": "john@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data

@patch('app.routes.auth_routes.User.query')
def test_get_all_users(mock_query, client):
    mock_query.all.return_value = [MagicMock(to_dict=lambda: {"id": 1, "username": "john", "email": "j@x.com"})]
    response = client.get('/auth/all')
    assert response.status_code == 200
    assert b'john' in response.data