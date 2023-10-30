from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from .db import Base


class DividendSchedule(Base):
    __tablename__ = 'dividend_schedule'
    id = Column(Integer(), primary_key=True)
    instrument = Column(String(10), unique=False, nullable=False)
    description = Column(String(100), unique=False, nullable=True)
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

    def __repr__(self):
        return (f"Portfolio {self.id} name={self.code} "
                f"description={self.description} "
                f"created_on={self.created_on} updated_on={self.updated_on}\n")
