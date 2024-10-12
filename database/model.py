from .database import Base
from sqlalchemy import Column, Integer, String, DateTime

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key= True, index= True)
    username = Column(String, unique= True, index= True)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="Subscriber")

class DbPost(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key= True, index= True)
    image_url = Column(String)
    title = Column(String)
    content = Column(String)
    creator = Column(String)
    timestamp = Column(DateTime)