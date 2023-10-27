from datetime import datetime
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime, ForeignKey)
from .db import Base


class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer(), primary_key=True)
    portfolio = Column(String(20), unique=False, nullable=True)
    instrument = Column(String(10), unique=False, nullable=False)
    quantity = Column(Numeric(12, 2))
    avg_price = Column(Numeric(12, 2))
    cost = Column(Numeric(12, 2))

    # realised pnl figures
    pnl_ytd = Column(Numeric(12, 2))
    pnl_last_year = Column(Numeric(12, 2))
    pnl_total = Column(Numeric(12, 2))

    div_ytd = Column(Numeric(12, 2))
    div_last_year = Column(Numeric(12, 2))
    div_total = Column(Numeric(12, 2))


    created_on = Column(DateTime(), default=datetime.now())
    updated_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now)

    def __repr__(self):
        return (f"Position {self.id} instrument={self.instrument} "
                f"quantity={self.quantity} avg_price={self.avg_price} "
                f"cost={self.cost} "
                f"pnl_ytd={self.pnl_ytd} pnl_last_year={self.pnl_last_year} pnl_total={self.pnl_total} "
                f"div_ytd={self.div_ytd} div_last_year={self.div_last_year} div_total={self.div_total} "                
                f"created_on={self.created_on} updated_on={self.updated_on}\n")

    def add_dividend(self, amount, payment_date):
        #if last year
        pass