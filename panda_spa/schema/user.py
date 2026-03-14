from typing import Optional

from pydantic import BaseModel, Field, field_validator

from panda_spa.validation.metaclasses import ServiceRegistryMeta


class UserSchema(BaseModel):
    name: str = Field(..., min_length=1, description="Name des Nutzers")
    species: str = Field(..., min_length=1, description="Spezies des Nutzers")
    favorite_service: Optional[str] = Field(
        None, description="Name des Lieblingsservice"
    )

    @field_validator("favorite_service")
    @classmethod
    def service_must_exist(cls, value):  # pylint: disable=no-self-argument
        if value is None:
            return value

        service_names = list(ServiceRegistryMeta.registry.keys())

        if value not in service_names:
            # pylint: disable=broad-exception-raised
            raise ValueError(f"booked service '{value}' does not exist")

        return value

    class Config:
        from_attributes = True
