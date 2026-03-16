from panda_spa.validation.descriptors import RangeValueDescriptor


class Dummy:
    value = RangeValueDescriptor("test.range")


def test_valid_value(monkeypatch):
    monkeypatch.setattr(
        "panda_spa.validation.descriptors.ConfigLoader.get",
        lambda path: {"min": 0, "max": 10}
    )

    obj = Dummy()
    obj.value = 5

    assert obj.value == 5
