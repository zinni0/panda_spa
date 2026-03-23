from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from panda_spa.db.database import Base


class FinanceEntry(Base):
    """
    Represents a financial entry in the system.

    :var type: The type of transaction (e.g., income, expense)
    :var amount: Transaction amount
    :var description: Description of the transaction
    :var date: Date and time of the transaction
    :var booking: Booking of the transaction
    """
    __tablename__ = "finance"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    booking_id = Column(
        Integer, ForeignKey("bookings.id", ondelete="CASCADE"), unique=True
    )

    booking = relationship("Booking", back_populates="finance_entry")
