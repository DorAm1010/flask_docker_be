from flask_jwt_extended import create_access_token
import pytest
from app.models.blog import Blog


@pytest.fixture
def new_blog_to_db(db):
    blog = Blog(title='Title', content='Content', image_url=None, user_id=1)
    db.session.add(blog)
    db.session.commit()
    return blog


def test_create_blog_post_unit(client, app, signup_user, login_user, get_user):
    token = create_access_token(identity=str(get_user.id))

    response = client.post("/blogs/create-blog", json={
        "title": "Unit Test Blog",
        "content": "Lorem ipsum",
        'user_id': get_user.id
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201

def test_get_blog_by_id_found(client, new_blog_to_db):
    blog_id = new_blog_to_db.id
    response = client.get(f'blogs/{blog_id}')
    assert response.status_code == 200, response.data
    assert response.json["title"] == new_blog_to_db.title

def test_delete_blog_found(client, db, signup_user, login_user, auth_headers, new_blog_to_db):
    blog_id = new_blog_to_db.id
    response = client.delete(f'/blogs/{blog_id}', headers=auth_headers)

    assert response.status_code == 200, response.data
    assert b"deleted successfully" in response.data
