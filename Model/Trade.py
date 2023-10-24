from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from .db import Base


class Trade(Base):
    __tablename__ = 'trade'
    id = Column(Integer(), primary_key=True)
    instrument = Column(String(10), unique=False, nullable=False)
    sedol = Column(String(10), unique=False, nullable=True)
    instrument_description = Column(String(100), unique=False, nullable=True)
    buy_sell = Column(String(1), unique=False, nullable=True)
    quantity = Column(Numeric(12, 2))
    price = Column(Numeric(12, 2))
    net_consideration = Column(Numeric(12, 2))
    trade_date = Column(DateTime())
    settle_date = Column(DateTime())
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)
