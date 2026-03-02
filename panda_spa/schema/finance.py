from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class FinanceSchema(BaseModel):
    type: str = Field(..., description="Typ: 'income' oder 'expense'")
    amount: float = Field(..., gt=0, description="Betrag muss positiv sein")
    description: Optional[str] = Field(None)
    date: datetime = Field(default_factory=datetime.utcnow)

    @validator("type")
    def type_must_be_valid(cls, v):
        if v not in ("income", "expense"):
            raise ValueError("Typ muss 'income' oder 'expense' sein")
        return v

    class Config:
        from_attributes = True
