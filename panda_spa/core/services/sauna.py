from typing import Dict, Any

from validation import RangeValueDescriptor

from .spa_service import SpaService


class Sauna(SpaService):
    _temperature = RangeValueDescriptor(
        config_path="spa_services.sauna.temperature"
    )

    def __init__(self, price: float, duration: int, temperature: int):
        super().__init__(price=price, duration=duration)
        self._temperature = temperature

    def get_description(self) -> str:
        return f"Sauna at {self._temperature}°C"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["temperature"] = self._temperature
        return base
