from typing import Dict, Any

from .spa_service import SpaService
from validation import RangeValueDescriptor


class ThermalBath(SpaService):
    _temperature = RangeValueDescriptor(
        config_path="spa_services.thermal_bath.temperature"
    )

    def __init__(self, price: float, duration: int, temperature: int):
        super().__init__(price=price, duration=duration)
        self._temperature = temperature

    def get_description(self) -> str:
        return f"Thermal bath at {self._temperature}°C"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["temperature"] = self._temperature
        return base
