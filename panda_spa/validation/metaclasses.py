import logging
from abc import ABCMeta
from typing import Type, Dict

logger = logging.getLogger(__name__)


class ServiceRegistryMeta(ABCMeta):
    """
    Metaclass that registers all subclasses into a registry except 'SpaService'.

    :var _registry (Dict[str, Type): Mapping of class names to class objects.
    """
    _registry: Dict[str, Type] = {}

    def __new__(mcs: Type[type], name: str, bases: tuple, dct: dict) -> type:
        """Register all classes except the base 'SpaService'"""
        cls_obj = super().__new__(mcs, name, bases, dct)
        if name != "SpaService":
            if name in ServiceRegistryMeta._registry:
                raise ValueError(f"Class {name} is already registered")

            logger.debug("Registering class %s", name)
            ServiceRegistryMeta._registry[name] = cls_obj
        return cls_obj

    @classmethod
    def get_registry(cls) -> Dict[str, Type]:
        """Returns a copy of the service registry"""
        return cls._registry.copy()
