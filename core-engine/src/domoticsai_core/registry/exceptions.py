class RegistryError(RuntimeError):
    pass

class RegistryFileError(RegistryError):
    pass

class RegistryValidationError(RegistryError):
    pass

class RegistryLookupError(RegistryError, KeyError):
    pass
