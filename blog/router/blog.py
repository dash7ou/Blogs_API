from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["blogs"],
    prefix="/blog"
)




@router.get("/", status_code=200, response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    try:
        blogs = db.query(models.Blog).all()
        return blogs
    except:
        raise HTTPException(status_code=500, detail=f'Something go wrong!')

@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
def get_one(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f'blog with id: {id} is not avalible')

    return blog

@router.post("/", status_code=201)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    try:
        new_blog = models.Blog(title= request.title, body=request.body, user_id=1)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Something go wrong!')

@router.put("/{id}", status_code=202)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f'Blog with id {id} not found')

    blog.update(request.dict(), synchronize_session=False)
    db.commit()

    return {
        "success": True
    }



@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f'Blog with id {id} not found')

    blog.delete(synchronize_session=False)
    db.commit()

    return {
        "success": True
    }
