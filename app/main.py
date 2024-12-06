from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app=FastAPI()


models.Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post('/create')
def create_post(req: schemas.CreateCalorieEvent, db: Session = Depends(get_session)):
    new_calorie_event = models.CalorieEvent(date=req.date, time=req.time, text=req.text, calories=req.noOfCalories)
    db.add(new_calorie_event)
    db.commit()
    db.refresh(new_calorie_event)

    return new_calorie_event


@app.get('/create')
def get_all(db: Session = Depends(get_session)):
    calorie_events = db.query(models.CalorieEvent).all()
    return calorie_events

@app.get('/create/{id}')
def show(id, db: Session = Depends(get_session)):
    calorie_event = db.query(models.CalorieEvent).filter(models.CalorieEvent.id == id).first()
    return calorie_event