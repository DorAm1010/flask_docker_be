from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import deferred
from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from models import db


# Base = declarative_base()

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True)
    title = Column(String(32), nullable=False)
    content = Column(String(128), nullable=False)
    image = Column(String(256))


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
