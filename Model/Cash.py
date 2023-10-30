import inspect
from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship, backref

from .db import Base


class Cash(Base):
    __tablename__ = 'cash'
    id = Column(Integer(), primary_key=True)
    type = Column(String(20))  # Deposit or Withdrawal or Interest or Initial
    description = Column(String(100), unique=False, nullable=True)
    amount = Column(Numeric(12, 2))
    payment_date = Column(DateTime(), nullable=False)
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

    portfolio_id = Column(Integer(), ForeignKey('portfolio.id'))
    portfolio = relationship("Portfolio",
                             backref=backref('cash', order_by='Cash.payment_date', cascade_backrefs=False)
                             )

    def __repr__(self):
        return (f"Cash {self.id} type={self.type} "
                f"description={self.description} a"
                f"mount={self.amount} "
                f"date={self.payment_date} "
                f"created_on={self.created_on} updated_on={self.updated_on}\n")
