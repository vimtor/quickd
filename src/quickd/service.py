from .inject import inject
from .singletons import constructors


def service(cls):
    if cls.__init__:
        cls.__init__ = inject(cls.__init__)
    constructors[cls] = cls
    return cls
