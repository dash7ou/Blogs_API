from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer, ForeignKey('users.id'))
    title = Column(String(200))
    body = Column(String(500))
    creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    email = Column(String(200)) 
    password = Column(String(2000)) 
    blogs = relationship("Blog", back_populates="creator") 