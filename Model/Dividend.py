from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship, backref

from .db import Base


class Dividend(Base):
    __tablename__ = 'dividend'
    id = Column(Integer(), primary_key=True)
    instrument = Column(String(10), unique=False, nullable=False)
    sedol = Column(String(10), unique=False, nullable=True)
    description = Column(String(100), unique=False, nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(DateTime(), nullable=False)
    portfolio_id = Column(Integer(), ForeignKey('portfolio.id'))
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

    portfolio_id = Column(Integer(), ForeignKey('portfolio.id'))
    portfolio = relationship("Portfolio",
                             backref=backref('dividend', order_by='Dividend.payment_date', cascade_backrefs=False)
                             )

    def __repr__(self):
        return (f"Dividend {self.id} instrument={self.instrument} sedol={self.sedol} "
                f"description={self.description} amount={self.amount} payment_date={self.payment_date} "
                f"created_on={self.created_on} updated_on={self.updated_on}\n")
