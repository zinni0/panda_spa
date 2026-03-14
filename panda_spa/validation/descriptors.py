from numbers import Real
from typing import Optional, Type

from panda_spa.core.config_loader import ConfigLoader


class ValidationError(Exception):
    pass


class RangeValueDescriptor:
    def __init__(self, config_path: str) -> None:
        self.__name: Optional[str] = None
        self.__config_path = config_path

    def __set_name__(self, owner: Type, name: str) -> None:
        self.__name = name

    def __get__(self, instance: Optional[object], owner: Type) -> Optional[Real]:
        if instance is None:
            return self
        return instance.__dict__.get(self.__name)

    def __set__(self, instance: object, value: Real) -> None:
        config = ConfigLoader.get(self.__config_path)

        min_value = config.get("min")
        max_value = config.get("max")

        if value is None:
            raise ValidationError(f"{self.__name} cannot be None")

        if not isinstance(value, Real):
            raise ValidationError(
                f"{self.__name} must be a numeric value, got {type(value).__name__}"
            )

        if min_value is not None and value < min_value:
            raise ValidationError(
                f"{self.__name} must be >= {min_value}, got {value}"
            )

        if max_value is not None and value > max_value:
            raise ValidationError(
                f"{self.__name} must be <= {max_value}, got {value}"
            )

        instance.__dict__[self.__name] = value
