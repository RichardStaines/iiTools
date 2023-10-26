from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from .db import Base


class Dividend(Base):
    __tablename__ = 'dividend'
    id = Column(Integer(), primary_key=True)
    instrument = Column(String(10), unique=False, nullable=False)
    sedol = Column(String(10), unique=False, nullable=True)
    description = Column(String(100), unique=False, nullable=True)
    amount = Column(Numeric(12, 2))
    trade_date = Column(DateTime())
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

    def __repr__(self):
        return (f"Dividend {self.id} instrument={self.instrument} sedol={self.sedol} "
                f"description={self.description} amount={self.amount} trade_date={self.trade_date} "
                f"created_on={self.created_on} updated_on={self.updated_on}\n")
