from fastapi import APIRouter, Depends
from schemas import schemas
from utils.database import get_db
from sqlalchemy.orm import Session
from repository import auth


router = APIRouter(
    tags=["Authentication"],
    prefix="/api/v1"
)

@router.post("/login", status_code=200, response_model=schemas.Token)
def login(request: schemas.Login, db: Session = Depends(get_db)):
    return auth.login(db, request)