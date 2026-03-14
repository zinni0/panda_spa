from sqlalchemy.orm import Session, joinedload

from panda_spa.models.booking import Booking
from panda_spa.schema.booking import BookingSchema


def create_booking(db: Session, booking: BookingSchema):
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
    return db.query(Booking).options(
        joinedload(Booking.user)
    ).order_by(Booking.start_time).all()
