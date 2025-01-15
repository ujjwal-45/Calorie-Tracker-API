from pydantic import BaseModel,EmailStr
from datetime import time,date
from typing import List


class CreateCalorieEvent(BaseModel):
    date:date
    time:time
    text:str
    noOfCalories:int

class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str


class ShowUser(BaseModel):
    username: str
    email: str
    role: str
    calorie_events : List[CreateCalorieEvent]
    class Config():
        from_attributes = True

class showCalorie(BaseModel):
    text: str
    noOfCalories:int
    creator: ShowUser

    class Config():
        from_attributes = True

