from typing import Dict, Any

from .spa_service import SpaService


class Massage(SpaService):
    def __init__(self, price: float, duration: int):
        super().__init__(price=price, duration=duration)

    def get_description(self) -> str:
        return "Massage"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        return base
