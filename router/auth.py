from fastapi import APIRouter, Depends
from schemas import schemas
from utils.database import get_db
from sqlalchemy.orm import Session
from repository import auth
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    tags=["Authentication"],
    prefix="/api/v1"
)

@router.post("/login", status_code=200, response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_login_details = schemas.Login(email= request.username, password=request.password)
    return auth.login(db, user_login_details)