from panda_spa.core.customer import Customer


def test_customer_creation():
    """
    Unit-Test für Customer-Klasse.
    Prüft, ob ein Customer korrekt initialisiert wird.
    Requirement: SR-03
    """
    # Arrange
    name = "Panda Paul"
    species = "Panda"

    # Act
    customer = Customer(name=name, species=species)

    # Assert
    assert customer.name == name
    assert customer.species == species
    assert isinstance(customer.customer_id, int)
