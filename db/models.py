from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from .database import Base


class Headline(Base):
    __tablename__ = 'headlines'

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(DateTime)
    time_stamp = Column(String)
    site = Column(String)
