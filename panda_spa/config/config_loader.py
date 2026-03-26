import logging
from pathlib import Path
from typing import Any

import yaml
from yaml import YAMLError

logger = logging.getLogger(__name__)


class ConfigLoader:
    _config: dict[str, Any] = {}
    _repo_root: Path = Path(__file__).parent.parent

    @classmethod
    def load(cls, path: str = None) -> None:
        """
        Load configuration from a YAML file

        :param path: Path to the YAML config file
        """
        if path is None:
            path = cls._repo_root / "config" / "services.yaml"
        else:
            path = Path(path)
            if not path.is_absolute():
                path = cls._repo_root / path

        try:
            with open(Path(path), "r", encoding="utf-8") as file:
                cls._config = yaml.safe_load(file) or {}
            logger.info("Config loaded from %s", path)
        except FileNotFoundError:
            logger.error("Config file not found: %s", path)
            raise
        except YAMLError as exc:
            logger.error("Invalid YAML format")
            raise exc

    @classmethod
    def get(cls, key_path: str, default: Any = None) -> Any:
        """
        Retrieve a value from the config using dot notation

        :param key_path: Dot-separated path (e.g. 'service.mail.host')
        :param default: Default value if key is not found
        :return: Config value or default
        """
        if not cls._config:
            raise RuntimeError("Config not loaded. Call 'load()' first")

        keys = key_path.split(".")
        current: Any = cls._config

        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            logger.warning("Config key not found: %s", key_path)
            return default

    @classmethod
    def clear(cls) -> None:
        """
        Clear the loaded configuration
        """
        cls._config = {}
