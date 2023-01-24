from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blog", status_code=200, response_model=List[schemas.ShowBlog], tags=["blogs"])
def get_all(db: Session = Depends(get_db)):
    try:
        blogs = db.query(models.Blog).all()
        return blogs
    except:
        raise HTTPException(status_code=500, detail=f'Something go wrong!')

@app.get("/blog/{id}", status_code=200, response_model=schemas.ShowBlog, tags=["blogs"])
def get_one(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f'blog with id: {id} is not avalible')

    return blog

@app.post("/blog", status_code=201, tags=["blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    try:
        new_blog = models.Blog(title= request.title, body=request.body, user_id=1)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Something go wrong!')

@app.put("/blog/{id}", status_code=202, tags=["blogs"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f'Blog with id {id} not found')

    blog.update(request.dict(), synchronize_session=False)
    db.commit()

    return {
        "success": True
    }



@app.delete("/blog/{id}", status_code=204, tags=["blogs"])
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f'Blog with id {id} not found')

    blog.delete(synchronize_session=False)
    db.commit()

    return {
        "success": True
    }


@app.post("/user", status_code=201, response_model=schemas.ShowUser, tags=["users"])
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

@app.get("/user/{id}", status_code=200, response_model=schemas.ShowUser, tags=["users"])
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=404, detail=f'User with id {id} not avalible')

    return user.first()
