from panda_spa.validation.descriptors import RangeValueDescriptor


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
