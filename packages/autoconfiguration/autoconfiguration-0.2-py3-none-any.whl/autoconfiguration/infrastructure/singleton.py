"""Contains the Singleton metaclass."""


class Singleton(type):
    """
    Metaclass to ensure that only one instance of a class is created.
    """

    _instances = {}
    _initialized = False

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            cls._initialized = True
        return cls._instances[cls]
