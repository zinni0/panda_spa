class ServiceRegistryMeta(type):
    registry = {}

    def __new__(cls, name, bases, dct):
        cls_obj = super().__new__(cls, name, bases, dct)
        if name != "SpaService":
            ServiceRegistryMeta.registry[name] = cls_obj
        return cls_obj
