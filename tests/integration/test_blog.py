# from flask_jwt_extended import create_access_token
# import pytest
# from app.models.user import User

import pytest
from app.models.blog import Blog
from app.models.user import User
from flask_jwt_extended import create_access_token




def test_create_blog(client, signup_user, login_user, get_user):
    # Register user
    user = get_user

    # token = login_res.get_json()['user']["token"]
    token = create_access_token(identity=str(user.id))
    # Authenticated request
    response = client.post("/blogs/create-blog", json={
        "title": "My First Blog",
        "content": "Exciting content",
        'user_id': user.id
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201, response.data
    assert b"My First Blog" in response.data

def test_get_all_blogs(client):
    response = client.get("/blogs/all")
    assert response.status_code == 200

def test_get_blog_by_id(client, app, signup_user, login_user, get_user, db):
    blog = Blog(title="Sample", content="Testing", image_url=None, user_id=1)
    db.session.add(blog)
    db.session.commit()
    response = client.get(f"/blogs/{blog.id}")
    assert response.status_code == 200
    assert b"Sample" in response.data

def test_get_user_blogs(client, auth_headers):
    response = client.get("/blogs/my-blogs", headers=auth_headers)
    assert response.status_code == 200

def test_update_blog(client, app, auth_headers, db):
    blog = Blog(title="Old", content="Old content", image_url=None, user_id=1)
    db.session.add(blog)
    db.session.commit()
    response = client.put(f"/blogs/{blog.id}", data={"title": "Updated"}, headers=auth_headers)
    assert response.status_code == 200
    assert b"updated successfully" in response.data

def test_delete_blog(client, app, auth_headers, db):
    blog = Blog(title="ToDelete", content="Gone soon", image_url=None, user_id=1)
    db.session.add(blog)
    db.session.commit()
    response = client.delete(f"/blogs/{blog.id}", headers=auth_headers)
    assert response.status_code == 200
    assert b"deleted successfully" in response.data
