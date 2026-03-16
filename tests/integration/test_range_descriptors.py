import pytest

from panda_spa.validation import RangeValueDescriptor, ValidationError


class Product:
    price = RangeValueDescriptor("validation.price")

    def __init__(self, price):
        self.price = price


def test_product_price_validation(monkeypatch):
    monkeypatch.setattr(
        "panda_spa.validation.descriptors.ConfigLoader.get",
        lambda path: {"min": 1, "max": 100}
    )

    product = Product(50)

    assert product.price == 50


def test_product_invalid_price(monkeypatch):
    monkeypatch.setattr(
        "panda_spa.validation.descriptors.ConfigLoader.get",
        lambda path: {"min": 10}
    )

    with pytest.raises(ValidationError):
        Product(5)
