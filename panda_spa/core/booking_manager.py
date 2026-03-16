from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple

from sqlalchemy import and_
from sqlalchemy.orm import Session

from panda_spa.db.crud import create_booking, create_user
from panda_spa.db.models import Booking
from panda_spa.schema import BookingSchema, UserSchema


@dataclass
class BookingFormData:
    name: str
    species: str
    date: str
    time: str
    service: str


class BookingManager:
    @staticmethod
    def create_booking(db: Session, data: BookingFormData) -> Tuple[int, str | None]:
        error = None

        booking_datetime = datetime.strptime(
            f"{data.date} {data.time}", "%Y-%m-%d %H:%M"
        )
        booking_endtime = booking_datetime + timedelta(minutes=30)

        if booking_datetime < datetime.now():
            error = "Buchung darf nicht in der Vergangenheit liegen"
            return 422, error

        overlapping = BookingManager.__find_bookings(
            db, booking_datetime, booking_endtime
        )

        if overlapping:
            error = "Es existiert bereits ein Termin in diesem Zeitraum"
            return 409, error

        user_schema = UserSchema(
            name=data.name,
            species=data.species,
            favorite_service=None
        )
        user = create_user(db, user_schema)

        booking_schema = BookingSchema(
            user_id=user.id,
            service_name=data.service,
            start_time=booking_datetime,
            end_time=booking_endtime
        )
        create_booking(db, booking_schema)

        return 200, error

    @staticmethod
    def __find_bookings(db: Session, start_time: datetime, end_time: datetime):
        return db.query(Booking).filter(
            and_(Booking.start_time < start_time, Booking.end_time > end_time)
        ).first()
