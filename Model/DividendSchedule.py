from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from .db import Base


class DividendSchedule(Base):
    __tablename__ = 'dividend_schedule'
    id = Column(Integer(), primary_key=True)
    instrument = Column(String(10), unique=False, nullable=False)
    ex_div_date = Column(DateTime())
    payment_date = Column(DateTime())
    payment = Column(Numeric(12, 2))
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

    def __repr__(self):
        return (f"Portfolio {self.id} instrument={self.instrument} "
                f"ex_div_date={self.ex_div_date} "
                f"payment_date={self.payment_date} "
                f"payment={self.payment} "
                f"created_on={self.created_on} updated_on={self.updated_on}\n")
