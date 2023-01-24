from fastapi import APIRouter, Depends, HTTPException
from schemas import schemas
from models import models
from utils.database import get_db
from sqlalchemy.orm import Session
from utils.hashing import Hash

router = APIRouter(
    tags=["users"],
    prefix="/user"
)



@router.post("/", status_code=201, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email)
    if user.first():
        raise HTTPException(status_code=400, detail=f'User already exist')

    hashed_pass = Hash.bcrypt(request.password)
    new_user = models.User(name = request.name, password= hashed_pass, email = request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code=200, response_model=schemas.ShowUser)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=404, detail=f'User with id {id} not avalible')

    return user.first()
