from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Literal

from pydantic import ValidationError
from sqlalchemy.orm import Session

from panda_spa.db.crud import set_booking_paid, get_booking_by_id, create_transaction
from panda_spa.schema import TransactionSchema


@dataclass
class FinanceFormData:
    type: Literal["income", "expense"]
    amount: float
    description: str


class FinanceManager:
    @staticmethod
    def create_transaction(
            db: Session,
            data: FinanceFormData,
            booking_id: int = None
    ) -> Tuple[int, str | None]:
        if FinanceManager._is_paid(db, booking_id):
            return 409, "invoice is already settled and cannot be charged again"

        try:
            transaction_schema = TransactionSchema(
                transaction_type=data.type,
                amount=data.amount,
                description=data.description,
                date=datetime.utcnow(),
                booking_id=booking_id
            )

        except ValidationError as exc:
            error_massages = "; ".join(
                [f"{err['loc'][0]}: {err['msg']}" for err in exc.errors()]
            )
            return 400, error_massages

        create_transaction(db, transaction_schema)

        if booking_id:
            set_booking_paid(db, booking_id)

        return 200, None

    @staticmethod
    def _is_paid(db: Session, booking_id: int | None) -> bool:
        if not booking_id:
            return False

        booking = get_booking_by_id(db, booking_id)
        return booking.is_paid
