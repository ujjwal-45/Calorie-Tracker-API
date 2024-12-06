from sqlalchemy import Column,String,Integer,Float,Date,Time,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=True)
    role = Column(String)

class CalorieEvent(Base):
    __tablename__ = 'calorie_events'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    text = Column(String)
    calories = Column(Float)