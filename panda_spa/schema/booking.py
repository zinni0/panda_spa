from datetime import datetime

from pydantic import BaseModel, validator, Field


class BookingSchema(BaseModel):
    user_id: int = Field(..., gt=0, description="ID des Nutzers")
    service_name: str = Field(..., description="Name des gebuchten Services")
    start_time: datetime = Field(..., description="Startzeit der Buchung")
    end_time: datetime = Field(..., description="Endzeit der Buchung")

    @validator("end_time")
    def end_must_be_after_start(cls, v, values):
        start = values.get("start_time")
        if start and v <= start:
            raise ValueError("Endzeit muss nach Startzeit liegen")
        return v

    @validator("service_name")
    def service_must_exist(cls, v, values, **kwargs):
        if v:
            service_names = [s.name for s in kwargs.get("services", [])]
            if v not in service_names:
                raise ValueError(f"Favorite service '{v}' existiert nicht")
        return v

    class Config:
        from_attributes = True
