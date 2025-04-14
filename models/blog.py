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


    def __init__(self, title, content, image):
        self.title = title
        self.content = content
        self.image = image

    def __repr__(self):
        return f'<Blog {self.title}>'
    
    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'image_url': self.image
        }
