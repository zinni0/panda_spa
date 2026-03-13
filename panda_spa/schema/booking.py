from datetime import datetime

from pydantic import BaseModel, validator, Field


class BookingSchema(BaseModel):
    user_id: int = Field(..., gt=0, description="ID des Nutzers")
    service_name: str = Field(..., description="Name des gebuchten Services")
    start_time: datetime = Field(..., description="Startzeit der Buchung")
    end_time: datetime = Field(..., description="Endzeit der Buchung")

    @validator("end_time")
    def end_must_be_after_start(cls, value, values):  # pylint: disable=no-self-argument
        start = values.get("start_time")
        if start and value <= start:
            raise ValueError("Endzeit muss nach Startzeit liegen")
        return value

    @validator("service_name")
    def service_must_exist(cls, value, _values, **kwargs):  # pylint: disable=no-self-argument
        if value:
            service_names = [s.name for s in kwargs.get("services", [])]
            if value not in service_names:
                # pylint: disable=broad-exception-raised
                raise ValueError(f"Favorite service '{value}' existiert nicht")
        return value

    class Config:
        from_attributes = True
