
import pytest
from app.app import create_app, db as _db
from flask_jwt_extended import JWTManager, create_access_token
from unittest.mock import patch
from app.models.user import User


@pytest.fixture(scope="module")
def app():
    app = create_app('sqlite:///:memory:')
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        jwt = JWTManager(app)
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope="module")
def client(app):
    return app.test_client()

@pytest.fixture(scope="module")
def db(app):
    return _db

@pytest.fixture(scope='module')
def new_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "newUser123!"
    }

@pytest.fixture()
def signup_user(client, new_user_data):
    client.post("/auth/signup", json=new_user_data)

@pytest.fixture()
def login_user(client, new_user_data):
    client.post("/auth/login", json={
        "email": new_user_data["email"],
        "password": new_user_data["password"]
    })

@pytest.fixture()
def get_user(db, new_user_data):
    return db.session.execute(
        db.select(User).
        filter_by(email=new_user_data['email']).
        limit(1)
        ).scalars().first()

@pytest.fixture
def auth_headers(get_user):
    token = create_access_token(identity=str(get_user.id))
    return {"Authorization": f"Bearer {token}"}
