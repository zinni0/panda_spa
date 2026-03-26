import logging
from typing import Optional, Set

from pydantic import BaseModel, Field, field_validator

from validation import ServiceRegistryMeta

logger = logging.getLogger(__name__)


class UserSchema(BaseModel):
    """
    Schema for user data validation.

    :var name: Name of the user, must not be empty.
    :var species: Species of the user, must not be empty.
    :var favorite_service: Optional favorite service name, must exist in the registry.
    """
    name: str = Field(..., min_length=1, description="Name of the user")
    species: str = Field(..., min_length=1, description="Species of the user")
    favorite_service: Optional[str] = Field(
        None, description="Name of the favorite service"
    )

    @classmethod
    def _get_service_names(cls) -> Set[str]:
        if not hasattr(cls, "_service_names"):
            registry = ServiceRegistryMeta.get_registry()
            cls._service_names = set(registry or [])
        return cls._service_names

    @field_validator("favorite_service")
    @classmethod
    def service_must_exist(cls, value: Optional[str]) -> Optional[
        str]:  # pylint: disable=no-self-argument
        """Ensure favorite_service exists in the service registry."""
        if value is None:
            return value

        service_names = cls._get_service_names()

        if value not in service_names:
            logger.warning("Attempted to assign non-existent service: %s", value)
            # pylint: disable=broad-exception-raised
            raise ValueError(f"booked service '{value}' does not exist")

        return value

    class Config:
        from_attributes = True
