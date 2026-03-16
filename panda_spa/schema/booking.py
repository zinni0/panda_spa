from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from panda_spa.validation import ServiceRegistryMeta


class BookingSchema(BaseModel):
    user_id: int = Field(..., gt=0, description="ID des Nutzers")
    service_name: str = Field(..., description="Name des gebuchten Services")
    start_time: datetime = Field(..., description="Startzeit der Buchung")
    end_time: datetime = Field(..., description="Endzeit der Buchung")

    @field_validator("end_time")
    @classmethod
    def end_must_be_after_start(cls, value, info):  # pylint: disable=no-self-argument
        start = info.data.get("start_time")
        if start and value <= start:
            # pylint: disable=broad-exception-raised
            raise ValueError("Endzeit muss nach Startzeit liegen")
        return value

    @field_validator("service_name")
    @classmethod
    def service_must_exist(cls, value):  # pylint: disable=no-self-argument
        if value is None:
            return value

        service_names = list(ServiceRegistryMeta.get_registry().keys())

        if value not in service_names:
            # pylint: disable=broad-exception-raised
            raise ValueError(f"booked service '{value}' does not exist")

        return value

    class Config:
        from_attributes = True
