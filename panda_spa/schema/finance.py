from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class FinanceSchema(BaseModel):
    type: str = Field(..., description="Typ: 'income' oder 'expense'")
    amount: float = Field(..., gt=0, description="Betrag muss positiv sein")
    description: Optional[str] = Field(None)
    date: datetime = Field(default_factory=datetime.utcnow)

    @validator("type")
    def type_must_be_valid(cls, value):  # pylint: disable=no-self-argument
        if value not in ("income", "expense"):
            # pylint: disable=broad-exception-raised
            raise ValueError("Typ muss 'income' oder 'expense' sein")
        return value

    class Config:
        from_attributes = True
