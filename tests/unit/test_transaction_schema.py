from datetime import datetime

import pytest
from pydantic import ValidationError

from panda_spa.schema import TransactionSchema  # Passe den Importpfad an


def test_valid_transaction():
    t = TransactionSchema(transaction_type="income", amount=100.0, description="Salary")
    assert t.transaction_type == "income"
    assert t.amount == 100.0
    assert t.description == "Salary"
    assert isinstance(t.date, datetime)  # default_factory gesetzt


def test_default_description_and_date():
    t = TransactionSchema(transaction_type="expense", amount=50.0)
    assert t.description == ""
    assert isinstance(t.date, datetime)


@pytest.mark.parametrize("invalid_type", ["gift", "", None, 123])
def test_invalid_transaction_type(invalid_type):
    with pytest.raises(ValidationError):
        TransactionSchema(transaction_type=invalid_type, amount=100.0)


@pytest.mark.parametrize("invalid_amount", [-100, 0, None])
def test_invalid_amount(invalid_amount):
    with pytest.raises(ValidationError):
        TransactionSchema(transaction_type="income", amount=invalid_amount)


def test_amount_and_type_edge_cases():
    t = TransactionSchema(transaction_type="expense", amount=0.01)
    assert t.amount == 0.01
