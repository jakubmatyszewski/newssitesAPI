from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime)

from .database import Base


class Tvn24(Base):
    __tablename__ = 'tvn24'
    id = Column(Integer, primary_key=True)
    headline = Column(DateTime)
    time_stamp = Column(String)


class Tvpinfo(Base):
    __tablename__ = 'tvpinfo'
    id = Column(Integer, primary_key=True)
    headline = Column(DateTime)
    time_stamp = Column(String)
