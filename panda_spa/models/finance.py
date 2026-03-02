from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from panda_spa.core.database import Base


class FinanceEntry(Base):
    __tablename__ = "finance"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)