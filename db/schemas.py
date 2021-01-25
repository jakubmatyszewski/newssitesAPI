from datetime import datetime

from pydantic import BaseModel


class SiteBase(BaseModel):
    id: int
    headline: str
    time_stamp: datetime

    class Config:
        orm_mode = True
