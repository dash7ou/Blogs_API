from pydantic import BaseModel
from typing import List


class BlogBase(BaseModel):
    title: str
    body: str



class Blog(BlogBase):
    class Config():
        orm_mode = True


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []
    
    class Config():
        orm_mode = True

class ShowUserBlog(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True

class ShowBlog(Blog):
    creator: ShowUserBlog
    class Config():
        orm_mode = True
 
class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None