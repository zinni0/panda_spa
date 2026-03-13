from abc import ABCMeta


class ServiceRegistryMeta(ABCMeta):
    registry = {}

    def __new__(mcs, name, bases, dct):
        cls_obj = super().__new__(mcs, name, bases, dct)
        if name != "SpaService":
            ServiceRegistryMeta.registry[name] = cls_obj
        return cls_obj
