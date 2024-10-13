from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
import datetime

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key= True, index= True)
    username = Column(String, unique= True, index= True)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="Subscriber")

class DbPost(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key= True, index= True)
    title = Column(String, index= True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default= datetime.datetime.now)
    updated_at = Column(DateTime, default= datetime.datetime.now)
    is_published = Column(Boolean, default= False)

    author = relationship('DbUser', back_populates= 'posts')

DbUser.posts = relationship('DbPost', back_populates= 'author')
