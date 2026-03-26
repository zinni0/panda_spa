from abc import ABC, abstractmethod
from typing import Any

from validation.metaclasses import ServiceRegistryMeta


class SpaService(ABC, metaclass=ServiceRegistryMeta):
    """
    Abstract class for all Spa-Services

    Subclasses must implement:
    - name (property)
    - get_description()
    """

    def __init__(self, price: float, duration: int) -> None:
        if price < 0:
            raise ValueError("price must be non-negative")
        if duration <= 0:
            raise ValueError("duration must be positive")

        self._price = price
        self._duration = duration

    @property
    def name(self) -> str:
        """Return the name of the service"""
        return type(self).__name__

    @abstractmethod
    def get_description(self) -> str:
        """Return a human-readable description of the service"""

    def to_dict(self) -> dict[str, Any]:
        """Serialize service to dictionary"""
        return {
            "service_type": type(self).__name__,
            "price": self._price,
            "duration": self._duration,
        }
