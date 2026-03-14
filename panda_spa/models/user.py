from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from panda_spa.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)

    favorite_service_name = Column(String, nullable=True)

    bookings = relationship("Booking", back_populates="user")
