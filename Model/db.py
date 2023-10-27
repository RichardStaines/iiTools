from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)

engine = create_engine("sqlite:///database/trading.sqlite")

Base = declarative_base()

from .Instrument import Instrument
from .Cash import Cash
from .Trade import Trade
from .Dividend import Dividend
from .Position import Position


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
