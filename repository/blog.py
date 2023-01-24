from sqlalchemy.orm import Session
from models import models
from fastapi import HTTPException
from schemas import schemas


def get_all(db: Session):
    try:
        blogs = db.query(models.Blog).all()
        return blogs
    except:
        raise HTTPException(status_code=500, detail=f'Something go wrong!')


def get_one(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f'blog with id: {id} is not avalible')

    return blog


def create(db: Session, request: schemas.Blog):
    try:
        new_blog = models.Blog(title= request.title, body=request.body, user_id=1)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Something go wrong!')


def update(db: Session, id: int, request: schemas.Blog):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f'Blog with id {id} not found')

    blog.update(request.dict(), synchronize_session=False)
    db.commit()

    return {
        "success": True
    }


def delete(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f'Blog with id {id} not found')

    blog.delete(synchronize_session=False)
    db.commit()

    return {
        "success": True
    }
