from typing import Dict, Any

from panda_spa.core.services.spa_service import SpaService
from panda_spa.validation.descriptors import RangeValueDescriptor


class ThermalBath(SpaService):
    temperature = RangeValueDescriptor(
        min_value=30,
        max_value=40
    )

    def __init__(self, price: float, duration: int, temperature: int):
        super().__init__(price=price, duration=duration)
        self.temperature = temperature

    def get_description(self) -> str:
        return f"Thermal bath at {self.temperature}°C"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["temperature"] = self.temperature
        return base
