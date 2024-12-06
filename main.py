from fastapi import FastAPI
from pydantic import BaseModel
from datetime import time,date



app=FastAPI()

@app.get('/')
def index():
    return {'data': {'name': 'me'}}

@app.get('/about')
def about(limit=10,correct=True):
    return {'data': f"{limit} are the no of contacts"}

@app.get('/blog/{id}')
def show(id):
    return {'data': id}

class CreateCalorieEvent(BaseModel):
    date:date
    time:time
    text:str
    noOfCalories:int

@app.post('/calorie_counter')
def calorie_counter(calorie:CreateCalorieEvent):
    return {'data': f"amount of calories{calorie} is insane"}


