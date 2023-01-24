from fastapi import APIRouter, Depends, HTTPException
from schemas import schemas
from models import models
from utils.database import get_db
from sqlalchemy.orm import Session
from repository import user

router = APIRouter(
    tags=["users"],
    prefix="/user"
)



@router.post("/", status_code=201, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(db, request)

@router.get("/{id}", status_code=200, response_model=schemas.ShowUser)
def get_user(id: int, db:Session = Depends(get_db)):
    return user.get_user(db, id)
