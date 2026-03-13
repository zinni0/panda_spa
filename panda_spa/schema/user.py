from typing import Optional

from pydantic import BaseModel, Field, validator


class UserSchema(BaseModel):
    name: str = Field(..., min_length=1, description="Name des Nutzers")
    species: str = Field(..., min_length=1, description="Spezies des Nutzers")
    favorite_service: Optional[str] = Field(
        None, description="Name des Lieblingsservice"
    )

    @validator("favorite_service")
    def service_must_exist(cls, v, values, **kwargs):
        if v:
            service_names = [s.name for s in kwargs.get("services", [])]
            if v not in service_names:
                raise ValueError(f"Favorite service '{v}' existiert nicht")
        return v

    class Config:
        from_attributes = True
