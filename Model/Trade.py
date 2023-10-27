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
    portfolio = Column(String(20), unique=False, nullable=True)
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

    def __repr__(self):
        return (f"Trade {self.id} instrument={self.instrument} sedol={self.sedol} "
                f"instrument_description={self.instrument_description} "
                f"buy_sell={self.buy_sell} quantity={self.quantity} price={self.price} "
                f"net_consideration={self.net_consideration} "
                f"trade_date={self.trade_date} settle_date={self.settle_date} "
                f"created_on={self.created_on} updated_on={self.updated_on}\n")