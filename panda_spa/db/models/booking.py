from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from .. import Base

class Booking(Base):
    """
    Represents a booking made by a user for a spa service.

    :var user_id: ID of the booking user
    :var service_name: Name of the booked service
    :var start_time: Start datetime of the booking
    :var end_time: End datetime of the booking
    :var is_paid: Boolean indicating if the booking has been paid
    True = paid, False = unpaid/open
    :var finance_entry: optional transaction of the booking
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_paid = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="bookings")

    finance_entry = relationship(
        "FinanceEntry",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan"
    )
