from sqlalchemy import Column, Integer, String
from .database import Base

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    body = Column(String(500))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    email = Column(String(200)) 
    password = Column(String(2000)) 