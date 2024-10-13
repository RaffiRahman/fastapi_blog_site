from sqlalchemy.orm import Session
from database import schemas, model

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = model.User(username=user.username, 
                         email=user.email, 
                         hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
