from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import deferred
from sqlalchemy import Column, ForeignKey, Integer, String
from app.models import db


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True)
    title = Column(String(32), nullable=False)
    content = Column(String(128), nullable=False)
    image_url = Column(String(256), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


    def __init__(self, title, content, image_url, user_id):
        self.title = title
        self.content = content
        self.image_url = image_url
        self.user_id = user_id

    def __repr__(self):
        return f'<Blog {self.title}>'
    
    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'image_url': self.image_url
        }
