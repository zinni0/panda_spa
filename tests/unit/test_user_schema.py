from unittest.mock import patch

import pytest
from pydantic import ValidationError

from panda_spa.schema import UserSchema

VALID_SERVICES = {"spa", "massage", "facial"}


@pytest.fixture
def mock_registry():
    with patch("panda_spa.validation.ServiceRegistryMeta.get_registry",
               return_value={name: None for name in VALID_SERVICES}):
        yield


def test_user_schema_valid(mock_registry):
    user = UserSchema(name="Alice", species="Human", favorite_service="spa")
    assert user.name == "Alice"
    assert user.species == "Human"
    assert user.favorite_service == "spa"


def test_user_schema_none_service(mock_registry):
    user = UserSchema(name="Bob", species="Elf", favorite_service=None)
    assert user.favorite_service is None


def test_user_schema_invalid_service(mock_registry):
    with pytest.raises(ValidationError) as exc_info:
        UserSchema(name="Charlie", species="Orc", favorite_service="invalid")

    errors = exc_info.value.errors()
    assert len(errors) == 1
    err = errors[0]
    assert err["type"] == "value_error"
    assert err["loc"] == ("favorite_service",)
    assert "booked service 'invalid' does not exist" in err["msg"]


def test_user_schema_empty_name(mock_registry):
    with pytest.raises(ValidationError):
        UserSchema(name="", species="Human", favorite_service="spa")


def test_user_schema_empty_species(mock_registry):
    with pytest.raises(ValidationError):
        UserSchema(name="Diana", species="", favorite_service="spa")
