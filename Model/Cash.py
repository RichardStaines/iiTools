from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from .db import Base


class Cash(Base):
    __tablename__ = 'cash'
    id = Column(Integer(), primary_key=True)
    type = Column(String(20))  # Deposit or Withdrawal or Interest or Initial
    description = Column(String(100), unique=False, nullable=True)
    amount = Column(Numeric(12, 2))
    date = Column(DateTime())
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

