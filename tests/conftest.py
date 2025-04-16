
import pytest
from app.app import create_app, db as _db
from flask_jwt_extended import JWTManager, create_access_token


@pytest.fixture(scope="module")
def app():
    app = create_app()
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
        "password": "123456"
    }
