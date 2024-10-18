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
    prefix='/post',
    tags=['post']
)

@router.post('/posts/', response_model= PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # user = db.query(DbUser).first()
    if not current_user:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return db_post.create(db, request, user_id=current_user.id)
    # return db_post.create(db, request)

@router.get('/posts/all')
def posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)

@router.delete('/posts/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_post.delete(id, db)

@router.post('/posts/image')
def upload_image(image: UploadFile = File(...), current_user: UserBase = Depends(get_current_user)):
    letter = string.ascii_letters
    randm_str = ''.join(random.choice(letter) for i in range(6))
    new = f'_{randm_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'


    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}