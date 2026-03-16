import pytest

from panda_spa.validation import RangeValueDescriptor, ValidationError


def test_valid_value(monkeypatch):
    monkeypatch.setattr(
        "panda_spa.validation.descriptors.ConfigLoader.get",
        lambda path: {"min": 0, "max": 10}
    )

    class Dummy:
        value = RangeValueDescriptor("test.range")

    obj = Dummy()
    obj.value = 5

    assert obj.value == 5


def test_value_below_min(monkeypatch):
    monkeypatch.setattr(
        "panda_spa.validation.descriptors.ConfigLoader.get",
        lambda path: {"min": 10}
    )

    class Dummy:
        value = RangeValueDescriptor("test.range")

    obj = Dummy()

    with pytest.raises(ValidationError):
        obj.value = 5


def test_invalid_type(monkeypatch):
    monkeypatch.setattr(
        "panda_spa.validation.descriptors.ConfigLoader.get",
        lambda path: {"min": 0}
    )

    class Dummy:
        value = RangeValueDescriptor("test.range")

    obj = Dummy()

    with pytest.raises(ValidationError):
        obj.value = "invalid"
