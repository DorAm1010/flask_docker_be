from flask import json
from flask_jwt_extended import create_access_token
import pytest
from sqlalchemy import select
from app.models.user import User

@pytest.fixture
def new_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": 'newUser123!'
    }

# def test_register_bad_password(client):
#     client.post("/auth/signup", json={
#         "username": "testuser",
#         "email": "test@example.com",
#         "password": "123456"
#     })
#     res = client.post("/auth/login", json={
#         "email": "test@example.com",
#         "password": "12345"
#     })
#     assert res.status_code == 409


def test_signup(client, new_user_data):
    res = client.post("/auth/signup", json=new_user_data)
    assert res.status_code == 201
    assert b"created successfully" in res.data

def test_login(client, new_user_data):
    res = client.post("/auth/login", json={
        "email": new_user_data["email"],
        "password": new_user_data["password"]
    })
    assert res.status_code == 200
    json_data = res.get_json()
    assert "token" in json_data["user"]

def test_update_user(client, app, db, new_user_data):
    res = client.post("/auth/login", json={
        "email": new_user_data["email"],
        "password": new_user_data["password"]
    })

    user = db.session.execute(
        select(User).
        filter_by(email="test@example.com").
        limit(1)
        ).scalars().first()

    # user = db.session.get(User, )
    token = create_access_token(identity=str(user.id))

    updated_data = {"username": "updateduser"}
    res = client.put(f"/auth/update/{user.id}", json=updated_data,
                     headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "User updated successfully, fields updated: username." in json.loads(res.data)['message']
    # user = db.session.execute(
    #     db.select(User).filter_by(email="test@example.com")).scalar_one_or_none()
    user = db.session.execute(
        select(User).
        filter_by(email="test@example.com").
        limit(1)
        ).scalars().first()
    assert "updateduser" == user.username

def test_delete_user(client, app, db):
    user = User.query.filter_by(email="test@example.com").first()
    token = create_access_token(identity=str(user.id))

    res = client.delete(f"/auth/delete/{user.id}",
                        headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

def test_login_wrong_password(client, new_user_data):
    # First register user
    client.post("/auth/signup", json=new_user_data)
    response = client.post("/auth/login", json={
        "email": new_user_data["email"],
        "password": new_user_data["email"][:-1]
    })
    assert response.status_code, 401
    assert "Invalid credentials" in json.loads(response.data)['message']

