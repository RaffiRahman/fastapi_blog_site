from typing import List
from fastapi import APIRouter, Depends, HTTPException
from auth import oauth2
from database.model import DbUser
from schemas import UserBase, UserDisplay, PostBase, PostDisplay
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_user, db_post
from database.hash import Hash
from auth.oauth2 import get_current_user, create_access_token
from auth import authentication
from fastapi import APIRouter, Depends, File, UploadFile
import string
import random
import shutil

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
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db_user.get_user_by_username(db=db, usernamel=username)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not Hash.verify(user.hashed_password, password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

