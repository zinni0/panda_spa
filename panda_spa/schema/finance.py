from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


class TransactionSchema(BaseModel):
    """
    Represents a financial transaction.

    :var transaction_type: The type of transaction, either 'income' or 'expense'
    :var amount: The monetary amount of the transaction; must be positive
    :var description: Optional text describing the transaction;
    defaults to an empty string
    :var date: The datetime of the transaction; defaults to the current UTC time
    """
    transaction_type: Literal["income", "expense"] = Field(
        ..., description="Type of transaction: 'income' or 'expense'"
    )
    amount: float = Field(..., gt=0, description="Amount must be positive")
    description: Optional[str] = Field(
        "", description="Optional description of the transaction"
    )
    date: datetime = Field(
        default_factory=datetime.utcnow, description="Transaction date"
    )

    booking_id: Optional[int] = Field(
        None, description="ID of the booking"
    )

    class Config:
        from_attributes = True
