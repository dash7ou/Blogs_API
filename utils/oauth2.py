from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .token import verify_token
from utils.database import get_db
from sqlalchemy.orm import Session
from models import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        email = verify_token(token)
        user = db.query(models.User).filter(models.User.email == email)
        if not user.first():
            raise Exception("User Not Found")
        return user.first()
    except JWTError:
        raise credentials_exception