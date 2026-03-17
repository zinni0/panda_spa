from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from panda_spa.db.database import Base


class Booking(Base):
    """
    Represents a booking made by a user for a spa service.

    :var user_id: ID of the booking user
    :var service_name: Name of the booked service
    :var start_time: Start datetime of the booking
    :var end_time: End datetime of the booking
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="bookings")
