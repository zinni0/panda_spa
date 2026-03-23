import logging
from datetime import datetime
from typing import Set, Optional

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from panda_spa.validation import ServiceRegistryMeta

logger = logging.getLogger(__name__)


class BookingSchema(BaseModel):
    """
    Schema for booking validation.

    :var user_id: ID of the user, must be greater than 0.
    :var service_name: Name of the booked service, must exist in the registry.
    :var start_time: Start time of the booking.
    :var end_time: End time of the booking, must be after start_time.
    :var is_paid: True if the booking has been paid, False if payment is still pending.
    :var transaction_id: Optional ID if booking has transaction.
    """
    user_id: int = Field(..., gt=0, description="id of the user")
    service_name: str = Field(..., description="name of the booked service")
    start_time: datetime = Field(..., description="start time of the booking")
    end_time: datetime = Field(..., description="end time of the booking")
    is_paid: bool = Field(
        default=False, description="True if the booking has been paid, False otherwise"
    )

    transaction_id: Optional[int] = None

    @classmethod
    def _get_service_names(cls) -> Set[str]:
        if not hasattr(cls, "_service_names"):
            registry = ServiceRegistryMeta.get_registry()
            cls._service_names = set(registry or [])
        return cls._service_names

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, value: datetime,
                          info: ValidationInfo) -> datetime:  # pylint: disable=no-self-argument
        start = info.data.get("start_time")
        if start is not None and value <= start:
            # pylint: disable=broad-exception-raised
            raise ValueError("end_time must be after start_time")
        return value

    @field_validator("service_name")
    @classmethod
    def validate_service_name(cls, value: str) -> str:  # pylint: disable=no-self-argument
        service_names = cls._get_service_names()

        if value not in service_names:
            logger.warning("Invalid service requested: %s", value)
            # pylint: disable=broad-exception-raised
            raise ValueError(f"booked service '{value}' does not exist")

        return value

    class Config:
        from_attributes = True
