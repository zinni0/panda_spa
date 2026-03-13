from abc import ABC, abstractmethod
from typing import Dict, Any

from panda_spa.validation.metaclasses import ServiceRegistryMeta


class SpaService(ABC, metaclass=ServiceRegistryMeta):
    """
    Abstract class for all Spa-Services
    """

    name: str
    price: float
    duration: int

    def __init__(self, price: float, duration: int) -> None:
        self.price = price
        self.duration = duration

    @abstractmethod
    def get_description(self) -> str:
        """Must be implemented from every Service"""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "service_type": self.__class__.__name__,
            "price": self.price,
            "duration": self.duration
        }
