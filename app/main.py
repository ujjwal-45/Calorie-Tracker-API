from fastapi import FastAPI, Depends, status, Response, HTTPException
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

@app.post('/create', status_code=status.HTTP_201_CREATED)
def create_post(req: schemas.CreateCalorieEvent, db: Session = Depends(get_session)):
    new_calorie_event = models.CalorieEvent(date=req.date, time=req.time, text=req.text, calories=req.noOfCalories)
    db.add(new_calorie_event)
    db.commit()
    db.refresh(new_calorie_event)

    return new_calorie_event


@app.delete('/create/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_calorie_event(id, db: Session = Depends(get_session)):
    calorie_event = db.query(models.CalorieEvent).filter(models.CalorieEvent.id == id)
    if not calorie_event.first():
        raise HTTPException(status_code=204, detail=f"Invalid query id:{id}")
    
    calorie_event.delete(synchronize_session=False)
    db.commit()
    return {'done'}


@app.put('/create/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, req: schemas.CreateCalorieEvent, db: Session = Depends(get_session)):
    calorie_event = db.query(models.CalorieEvent).filter(models.CalorieEvent.id == id)
    if not calorie_event.first():
        raise HTTPException(status_code=404, detail=f"Invalid query id:{id}")
    
    calorie_event.update({"text":"meat", "calories":600})
    db.commit()
    return "updated calories table"


@app.get('/create')
def get_all(db: Session = Depends(get_session)):
    calorie_events = db.query(models.CalorieEvent).all()
    return calorie_events



@app.get('/create/{id}')
def show(id,response:Response, db: Session = Depends(get_session)):
    calorie_event = db.query(models.CalorieEvent).filter(models.CalorieEvent.id == id).first()
    if not calorie_event:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail" : f"This calorie with id:{id} is not there."}
    return calorie_event


@app.post('/user')
def create_user(req:schemas.User, db: Session = Depends(get_session)):
    new_user = models.User(username = req.username, password = req.password, email = req.email, role = req.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user