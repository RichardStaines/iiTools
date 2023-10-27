from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from .db import Base


class Instrument(Base):
    __tablename__ = 'instrument'
    id = Column(Integer(), primary_key=True)
    code = Column(String(10), unique=False, nullable=False)
    sedol = Column(String(10), unique=False, nullable=True)
    description = Column(String(100), unique=False, nullable=True)
    price_source = Column(String(20), unique=False, nullable=True)
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

    def __repr__(self):
        return (f"Instrument {self.id} code={self.code} sedol={self.sedol} "
                f"description={self.description} price_source={self.price_source} "
                f"created_on={self.created_on} updated_on={self.updated_on}\n")
