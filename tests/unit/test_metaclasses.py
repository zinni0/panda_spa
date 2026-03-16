import pytest

from panda_spa.validation.metaclasses import ServiceRegistryMeta


# Dummy-Basisklasse
class SpaService(metaclass=ServiceRegistryMeta):
    pass


# Testklasse für Registrierung
class MassageService(SpaService):
    pass


class FacialService(SpaService):
    pass


def test_registry_excludes_base_class():
    registry = ServiceRegistryMeta.get_registry()
    assert 'SpaService' not in registry


def test_registry_includes_subclasses():
    registry = ServiceRegistryMeta.get_registry()
    assert 'MassageService' in registry
    assert 'FacialService' in registry


def test_registry_contains_correct_class_objects():
    registry = ServiceRegistryMeta.get_registry()
    assert registry['MassageService'] is MassageService
    assert registry['FacialService'] is FacialService


def test_double_registration_raises_error():
    class DummyService(SpaService):
        pass

    with pytest.raises(ValueError):
        ServiceRegistryMeta._registry['DummyService'] = DummyService
        ServiceRegistryMeta.__new__(ServiceRegistryMeta, 'DummyService', (SpaService,), {})
