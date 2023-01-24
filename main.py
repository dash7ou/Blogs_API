from fastapi import FastAPI
from models import models
from utils.database import engine
from router import blog, user, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog.router)

models.Base.metadata.create_all(engine)