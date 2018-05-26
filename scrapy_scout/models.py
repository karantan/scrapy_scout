from scrapy_scout import settings
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def db_connect():
    """Performs database connection using database settings from settings.py.

    Returns sqlalchemy engine instance
    """
    return create_engine(settings.DATABASE)


def create_tables(engine):
    """Creates priglasitve table."""
    Base.metadata.create_all(engine)


class Priglasitev(Base):
    """Sqlalchemy Priglasitev model"""
    __tablename__ = 'priglasitve'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)

    date = Column(Date, nullable=True)
    priglasitelj = Column(Unicode(250), nullable=True)
    privzeto_podjetje = Column(Unicode(250), nullable=True)
    sektor = Column(Unicode(250), nullable=True)
    st_zadeve = Column(Unicode(250), nullable=True)
