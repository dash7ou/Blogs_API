from sqlalchemy.orm import Session
from models import models
from fastapi import HTTPException
from schemas import schemas
from utils.hashing import Hash



def create(db: Session, request: schemas.User):
    user = db.query(models.User).filter(models.User.email == request.email)
    if user.first():
        raise HTTPException(status_code=400, detail=f'User already exist')

    hashed_pass = Hash.bcrypt(request.password)
    new_user = models.User(name = request.name, password= hashed_pass, email = request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



def get_user(db:Session, id: int):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=404, detail=f'User with id {id} not avalible')

    return user.first()