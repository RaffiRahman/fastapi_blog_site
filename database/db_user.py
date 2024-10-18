from fastapi import Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from database import model
from database.database import get_db
from schemas import UserBase
from database.hash import Hash

def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(model.DbUser).filter(model.DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {username} not found!")
    return user

def create_user(db: Session, request: UserBase):
    new_user = model.DbUser(
        username=request.username, 
        email=request.email, 
        hashed_password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

