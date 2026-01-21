from typing import Optional, Type


class RangeValueDescriptor:
    def __init__(self, name: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> None:
        self.__name = name
        self.__min_value = min_value
        self.__max_value = max_value

    def __get__(self, instance: Optional[object], owner: Type) -> Optional[int]:
        if instance is None:
            return self
        return instance.__dict__.get(self.__name)

    def __set__(self, instance: object, value: int) -> None:
        if value is None:
            raise ValueError(f"{self.__name} cannot be None")

        if self.__min_value is not None and value < self.__min_value:
            raise ValueError(
                f"{self.__name} must be >= {self.__min_value}, got {value}"
            )

        if self.__max_value is not None and value > self.__max_value:
            raise ValueError(
                f"{self.__name} must be <= {self.__max_value}, got {value}"
            )

        instance.__dict__[self.__name] = value
