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

