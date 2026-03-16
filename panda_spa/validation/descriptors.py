import logging
from numbers import Real
from typing import Optional, Type

from panda_spa.core.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when validation of a descriptor value fails."""
    pass


class RangeValueDescriptor:
    """
    Descriptor that validates numeric values against a configurable range.

    The valid range (min and max) is loaded from the configuration
    via ConfigLoader using the provided config_path.
    """

    def __init__(self, config_path: str) -> None:
        self._name: Optional[str] = None
        self._config = ConfigLoader.get(config_path)

    def __set_name__(self, owner: Type, name: str) -> None:
        """Store the attribute name when the descriptor is assigned."""
        self._name = name

    def __get__(self, instance: Optional[object], owner: Type) -> Optional[Real]:
        """Return the stored value."""
        if instance is None:
            return self
        return instance.__dict__.get(self._name)

    def __set__(self, instance: object, value: Real) -> None:
        """Validate and set the value."""
        min_value = self._config.get("min")
        max_value = self._config.get("max")

        logger.debug("Validating value %s for %s", value, self._name)

        if value is None:
            raise ValidationError(f"{self._name} cannot be None")

        if not isinstance(value, Real):
            raise ValidationError(
                f"'{self._name}' must be a numeric value, got {type(value).__name__}"
            )

        if min_value is not None and value < min_value:
            raise ValidationError(
                f"'{self._name}' must be >= {min_value}, got {value}"
            )

        if max_value is not None and value > max_value:
            raise ValidationError(
                f"'{self._name}' must be <= {max_value}, got {value}"
            )

        instance.__dict__[self._name] = value
