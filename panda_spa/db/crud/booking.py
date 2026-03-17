import logging
from typing import Tuple

from sqlalchemy.orm import Session, joinedload

from panda_spa.db.models import Booking
from panda_spa.schema import BookingSchema

logger = logging.getLogger(__name__)


def create_booking(db: Session, booking: BookingSchema) -> Booking:
    """
    Create a new booking in the database

    :param db: SQLAlchemy session object
    :param booking: Booking data to create
    :return: The newly created booking object
    """
    db_booking = Booking(
        user_id=booking.user_id,
        service_name=booking.service_name,
        start_time=booking.start_time,
        end_time=booking.end_time
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking


def get_bookings(db: Session):
    """
    Return all bookings with joined user info, ordered by start_time

    :param db: SQLAlchemy session object
    :return: List of Booking objects
    """
    return db.query(Booking).options(
        joinedload(Booking.user)
    ).order_by(Booking.start_time).all()


def delete_bookings(db: Session, booking_id: int) -> Tuple[str, str]:
    """
    Delete a booking by its ID

    :param db: SQLAlchemy session object
    :param booking_id: ID of the booking to delete
    :return: Tuple containing status ('success' or 'error') and a message
    """
    booking = db.query(Booking).get(booking_id)
    if booking:
        db.delete(booking)
        db.commit()
        logger.info("Booking %s deleted", booking_id)
        return "success", f"Booking {booking_id} deleted"

    logger.warning("Booking %s not found", booking_id)
    return "error", "Booking not found"
