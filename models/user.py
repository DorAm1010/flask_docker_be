from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import deferred
from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from models import db


# Base = declarative_base()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = deferred(Column(String(128), nullable=False))


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
