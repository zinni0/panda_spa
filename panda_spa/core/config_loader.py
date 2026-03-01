from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:
    __config: dict[str, Any] = {}

    @classmethod
    def load(cls, path: str) -> None:
        with open(Path(path), "r", encoding="utf-8") as file:
            cls.__config = yaml.safe_load(file)

    @classmethod
    def get(cls, key_path: str) -> Any:
        keys = key_path.split(".")
        value = cls.__config
        for key in keys:
            value = value[key]
        return value
