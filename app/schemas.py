from pydantic import BaseModel,EmailStr
from datetime import time,date

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