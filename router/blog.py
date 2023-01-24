from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas import schemas
from utils.database import get_db
from sqlalchemy.orm import Session
from repository import blog

router = APIRouter(
    tags=["blogs"],
    prefix="/blog"
)




@router.get("/", status_code=200, response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
def get_one(id: int, db: Session = Depends(get_db)):
    return blog.get_one(db, id)

@router.post("/", status_code=201)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(db, request)

@router.put("/{id}", status_code=202)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(db, id, request)



@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    return blog.delete(db, id)