from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from database.database import get_db
from database import model
from database.hash import Hash
from auth import oauth2


router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.DbUser).filter(model.DbUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid username")
    
    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Invalid Password")
    
    access_token = oauth2.create_access_token(data= {'sub': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'email': user.email,
        'username': user.username
    }