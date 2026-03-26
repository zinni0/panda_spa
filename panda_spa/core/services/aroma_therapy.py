from typing import Dict, Any

from validation import RangeValueDescriptor

from .spa_service import SpaService


class AromaTherapy(SpaService):
    _intensity = RangeValueDescriptor(
        config_path="spa_services.aroma_therapy.intensity"
    )

    def __init__(self, price: float, duration: int, intensity: int):
        super().__init__(price=price, duration=duration)
        self._intensity = intensity

    def get_description(self) -> str:
        return f"Aroma therapy at {self._intensity} intensity"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["intensity"] = self._intensity
        return base
