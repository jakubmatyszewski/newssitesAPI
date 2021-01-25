from datetime import datetime
from fastapi import Depends, FastAPI
from typing import List, Union


from sqlalchemy.orm import Session
from db import models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# https://stackoverflow.com/questions/42552696/sqlalchemy-nearest-datetime
@app.get("/news", response_model=List[schemas.SiteBase])
def get_news(
        date: Union[str, datetime] = datetime.now(),
        db: Session = Depends(get_db),
        site: str = 'tvn24',
        limit: int = 1):
    sites = {'tvn24': models.Tvn24, 'tvpinfo': models.Tvpinfo}
    if isinstance(date, str):
        if len(date) <= 10:
            date += 'T12:00:00'
        date = datetime.strptime(date[:19], '%Y-%m-%dT%H:%M:%S')
    return db.query(sites[site]).filter(sites[site].time_stamp <= date).\
        order_by(sites[site].time_stamp.desc()).limit(limit).all()


@app.get("/")
async def root():
    return {"message": "Hello World"}
