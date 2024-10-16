from typing import List
from fastapi import APIRouter, Depends, HTTPException
from auth import oauth2
from database.model import DbUser
from schemas import UserBase, UserDisplay, PostBase, PostDisplay
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_user, db_post
from auth.oauth2 import get_current_user, create_access_token
from auth import authentication

router = APIRouter(
    prefix='/api',
    tags=['api']
)

@router.post('/auth/register', response_model= UserDisplay)
def register(request: UserBase, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.email == request.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user.create_user(db, request)

@router.post('/auth/login')
def login(email: str, password: str, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    user = db_user.get_user_by_email(db=db, email=email)
    if not user or user.hashed_password != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post('/posts/', response_model= UserDisplay)
def create(request: PostBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    user = db.query(DbUser).first()
    if not user:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return db_post.create(db, request)
