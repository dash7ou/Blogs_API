from fastapi import FastAPI
from models import models
from utils.database import engine
from router import blog, user

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)