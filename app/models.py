from sqlalchemy import Column,String,Integer,Float,Date,Time,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class CalorieEvent(Base):
    __tablename__ = 'calorie_events'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    time = Column(Time)
    text = Column(String)
    calories = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="calorie_events")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)

    calorie_events = relationship("CalorieEvent", back_populates="owner")