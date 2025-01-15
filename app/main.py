from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash
import logging


app=FastAPI()


models.Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



@app.post('/create', status_code=status.HTTP_201_CREATED, tags=['calories'])
def create_post(req: schemas.CreateCalorieEvent, db: Session = Depends(get_session)):
    new_calorie_event = models.CalorieEvent(date=req.date, time=req.time, text=req.text, calories=req.noOfCalories, user_id=1)
    db.add(new_calorie_event)
    db.commit()
    db.refresh(new_calorie_event)

    return new_calorie_event


@app.delete('/create/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['calories'])
def delete_calorie_event(id, db: Session = Depends(get_session)):
    calorie_event = db.query(models.CalorieEvent).filter(models.CalorieEvent.id == id)
    if not calorie_event.first():
        raise HTTPException(status_code=204, detail=f"Invalid query id:{id}")
    
    calorie_event.delete(synchronize_session=False)
    db.commit()
    return {'done'}


@app.put('/create/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['calories'])
def update(id, req: schemas.CreateCalorieEvent, db: Session = Depends(get_session)):
    calorie_event = db.query(models.CalorieEvent).filter(models.CalorieEvent.id == id)
    if not calorie_event.first():
        raise HTTPException(status_code=404, detail=f"Invalid query id:{id}")
    
    calorie_event.update({"text":"meat", "calories":600})
    db.commit()
    return "updated calories table"


@app.get('/create', tags=['calories'])
def get_all(db: Session = Depends(get_session)):
    calorie_events = db.query(models.CalorieEvent).all()
    return calorie_events



@app.get('/create/{id}', tags=['calories'], response_model=schemas.showCalorie)
def show(id: int, db: Session = Depends(get_session)):
    calorie_event = db.query(models.CalorieEvent).filter(models.CalorieEvent.id == id).first()
    
    user = db.query(models.User).filter(models.User.id == calorie_event.user_id).first()
    if not calorie_event:
        raise HTTPException(status_code=404, detail= f"This calorie with id:{id} is not there.")
    
    response = schemas.showCalorie(
        text=calorie_event.text,
        noOfCalories=calorie_event.calories,
        creator=schemas.ShowUser(
            username=user.username,
            email=user.email,
            role=user.role
        )
    )
    return response



@app.post('/user', response_model = schemas.ShowUser, tags=['users'])
def create_user(req:schemas.User, db: Session = Depends(get_session)):
    new_user = models.User(username = req.username, password = Hash.encrypt(req.password), email = req.email, role = req.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user/{id}',response_model=schemas.ShowUser ,tags=['users'])
def get_user(id: int,db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"user not found")
    
    calorie_events = [
        schemas.CreateCalorieEvent(
            date=event.date,
            time=event.time,
            text=event.text,
            noOfCalories=event.calories
        )
        for event in user.calorie_events
    ]

    return schemas.ShowUser(
        username=user.username,
        email=user.email,
        role=user.role,
        calorie_events=calorie_events
    )