from typing import Optional

from pydantic import BaseModel, Field, validator


class UserSchema(BaseModel):
    name: str = Field(..., min_length=1, description="Name des Nutzers")
    species: str = Field(..., min_length=1, description="Spezies des Nutzers")
    favorite_service: Optional[str] = Field(
        None, description="Name des Lieblingsservice"
    )

    @validator("favorite_service")
    def service_must_exist(cls, value, _values, **kwargs):  # pylint: disable=no-self-argument
        if value:
            service_names = [s.name for s in kwargs.get("services", [])]
            if value not in service_names:
                # pylint: disable=broad-exception-raised
                raise ValueError(f"Favorite service '{value}' existiert nicht")
        return value

    class Config:
        from_attributes = True
