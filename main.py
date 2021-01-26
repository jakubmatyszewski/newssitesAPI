from datetime import datetime
from typing import List, Union
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from db import models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# https://stackoverflow.com/questions/42552696/sqlalchemy-nearest-datetime
@app.get("/news", response_model=List[schemas.SiteBase])
def get_news(date: Union[str, datetime] = datetime.now(),
             db: Session = Depends(get_db),
             site: str = 'tvn24',
             limit: int = 1):
    sites = {'tvn24': models.Tvn24, 'tvpinfo': models.Tvpinfo}
    if isinstance(date, str):
        date_format = '%Y-%m-%dT%H:%M:%S'
        if len(date) <= 10:
            date += 'T12:00:00'
        else:
            date_format = date_format[:len(date) - 2]
        date = datetime.strptime(date[:19], date_format)
    return db.query(sites[site]).filter(sites[site].time_stamp <= date).\
        order_by(sites[site].time_stamp.desc()).limit(limit).all()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/")
async def form_submit(request: Request,
                      db: Session = Depends(get_db),
                      date: str = Form(...),
                      site: str = Form(...)):
    results = get_news(date=date,
                       db=db,
                       site=site)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": results}
    )
