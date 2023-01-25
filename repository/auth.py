from sqlalchemy.orm import Session
from models import models
from fastapi import HTTPException
from schemas import schemas
from utils.hashing import Hash
from utils.token import create_access_token 



def login(db: Session, request: schemas.Login):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail=f'Invalid Credentials')

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=400, detail=f'Incorrect Password')

    access_token = create_access_token(
        data={"sub": request.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

    
