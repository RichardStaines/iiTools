from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)

DEFAULT_CONNECTION_STR = "sqlite:///database/trading.sqlite"

Base = declarative_base()

class DataAccessLayer:

    def __int__(self):
        self.engine = None
        self.connection_str = ""
        self.session = None

    def connect(self, connection_str=DEFAULT_CONNECTION_STR):
        self.engine = create_engine(connection_str)
        Base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.session_maker()  # this creates a session


from .Portfolio import Portfolio
from .Instrument import Instrument
from .Cash import Cash
from .Trade import Trade
from .Dividend import Dividend
from .Position import Position
from .DividendSchedule import DividendSchedule


data_access_layer = DataAccessLayer()

