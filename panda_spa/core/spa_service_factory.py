import re

from .services.spa_service import SpaService
from config import ConfigLoader
from validation import ServiceRegistryMeta


class SpaServiceFactory:
    @staticmethod
    def _class_to_config_name(class_name: str) -> str:
        """Convert PascalCase -> snake_case"""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()

    @classmethod
    def create(cls, class_name: str) -> SpaService:
        """
        Create an instance of a SpaService subclass from its name,
        using the loaded configuration.

        :param class_name: Name of the service class
        :return: Instance of the service
        """
        registry = ServiceRegistryMeta.get_registry()

        service_cls = registry.get(class_name)

        if service_cls is None:
            raise ValueError(f"Unknown SpaService class: {class_name}")

        config_name = cls._class_to_config_name(class_name)

        price = ConfigLoader.get(f"spa_services.{config_name}.price")
        duration = ConfigLoader.get(f"spa_services.{config_name}.duration")

        if price is None or duration is None:
            raise ValueError(f"Missing configuration for {config_name}")

        extra_params = ConfigLoader.get(f"spa_services.{config_name}.extra", {})
        if not isinstance(extra_params, dict):
            extra_params = {}

        return service_cls(price=price, duration=duration, **extra_params)
