from numbers import Real
from typing import Optional, Type


class ValidationError(Exception):
    pass


class RangeValueDescriptor:
    def __init__(
            self,
            *,
            min_value: Optional[Real] = None,
            max_value: Optional[Real] = None
    ) -> None:
        self.__name: Optional[str] = None
        self.__min_value = min_value
        self.__max_value = max_value

    def __set_name__(self, owner: Type, name: str) -> None:
        self.__name = name

    def __get__(self, instance: Optional[object], owner: Type) -> Optional[Real]:
        if instance is None:
            return self
        return instance.__dict__.get(self.__name)

    def __set__(self, instance: object, value: Real) -> None:
        if value is None:
            raise ValidationError(f"{self.__name} cannot be None")

        if not isinstance(value, Real):
            raise ValidationError(
                f"{self.__name} must be a numeric value, got {type(value).__name__}"
            )

        if self.__min_value is not None and value < self.__min_value:
            raise ValidationError(
                f"{self.__name} must be >= {self.__min_value}, got {value}"
            )

        if self.__max_value is not None and value > self.__max_value:
            raise ValidationError(
                f"{self.__name} must be <= {self.__max_value}, got {value}"
            )

        instance.__dict__[self.__name] = value
