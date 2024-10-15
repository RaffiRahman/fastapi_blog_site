from random import SystemRandom
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str

class PostDisplay(BaseModel):
    id: int
    title: str
    content: str
    author: UserDisplay
    class Config:
        from_attributes = True
    
