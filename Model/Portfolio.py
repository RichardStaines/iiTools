from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from .db import Base


class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer(), primary_key=True)
    name = Column(String(10), unique=True, nullable=False)
    description = Column(String(100), unique=False, nullable=True)
    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

    def __repr__(self):
        return (f"Portfolio {self.id} name={self.name} "
                f"description={self.description} "
                f"created_on={self.created_on} updated_on={self.updated_on}\n")
