from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blog", status_code=200, response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    try:
        blogs = db.query(models.Blog).all()
        return blogs
    except:
        raise HTTPException(status_code=500, detail=f'Something go wrong!')

@app.get("/blog/{id}", status_code=200, response_model=schemas.ShowBlog)
def get_one(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f'blog with id: {id} is not avalible')

    return blog

@app.post("/blog", status_code=201)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    try:
        new_blog = models.Blog(title= request.title, body=request.body)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except:
        raise HTTPException(status_code=500, detail=f'Something go wrong!')

@app.put("/blog/{id}", status_code=202)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    print(request)
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f'Blog with id {id} not found')

    blog.update(request.dict(), synchronize_session=False)
    db.commit()

    return {
        "success": True
    }



@app.delete("/blog/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f'Blog with id {id} not found')

    blog.delete(synchronize_session=False)
    db.commit()

    return {
        "success": True
    }

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/user")
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_pass = pwd_cxt.hash(request.password)
    new_user = models.User(name = request.name, password= hashed_pass, email = request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user  