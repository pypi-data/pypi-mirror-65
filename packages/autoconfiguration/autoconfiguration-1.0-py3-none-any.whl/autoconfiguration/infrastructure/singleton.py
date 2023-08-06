"""Contains the Singleton metaclass."""


class Singleton(type):
    """
    Metaclass to ensure that only one instance of the :class:`Config` class is created.
    """

    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance
