from pydantic import BaseModel
from datetime import time,date

class CreateCalorieEvent(BaseModel):
    date:date
    time:time
    text:str
    noOfCalories:int
