from abc import ABC, abstractmethod
from typing import Any

from panda_spa.validation.metaclasses import ServiceRegistryMeta


class SpaService(ABC, metaclass=ServiceRegistryMeta):
    """
    Abstract class for all Spa-Services

    Subclasses must implement:
    - name (property)
    - get_description()
    """

    def __init__(self, price: float, cost: float, duration: int) -> None:
        if price < 0:
            raise ValueError("price must be non-negative")
        if cost < 0:
            raise ValueError("cost must be non-negative")
        if duration <= 0:
            raise ValueError("duration must be positive")

        self.price = price
        self.cost = cost
        self.duration = duration

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the service"""

    @property
    def profit(self) -> float:
        return self.price - self.cost

    @abstractmethod
    def get_description(self) -> str:
        """Return a human-readable description of the service"""

    def to_dict(self) -> dict[str, Any]:
        """Serialize service to dictionary"""
        return {
            "service_type": type(self).__name__,
            "name": self.name,
            "price": self.price,
            "cost": self.cost,
            "duration": self.duration,
        }
